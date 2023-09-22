from django.shortcuts import render, redirect
from django import forms
from django.views import View
from django.views.generic import DetailView
from shop.forms import OrderForm
from shop.models import Product, Category, ProductOption, Order, OrderDetails
from django_filters import FilterSet, OrderingFilter, CharFilter, RangeFilter, ModelMultipleChoiceFilter
from django_filters.views import FilterView
from shop.utils import DataMixin, CartMixin


class ProductFilter(FilterSet):
    order = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('name', 'name'),
            ('price', 'price'),
        ),

        # labels do not need to retain order
        field_labels={
            'name': 'Наименование',
            'price': 'Цена',
        },
        label="Сортировать"
    )
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Наименование')
    price = RangeFilter(field_name='price', label='Цена')
    categories = ModelMultipleChoiceFilter(field_name='categories', queryset=Category.objects.all(),
                                           widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Product
        fields = [
            'order',
            'name',
            'club',
            'categories',
            'price'
        ]


class ProductList(DataMixin, FilterView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'product_list'
    filterset_class = ProductFilter


class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = 'shop/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        if obj.option_values.all():
            context['option_name'] = obj.option_values.first().option
            context['option_values'] = obj.option_values.filter(option=context['option_name']).all()
        return context

    def post(self, request, product_slug):
        product = request.POST.get('product')
        quantity_post = int(request.POST.get('quantity'))
        selected_option = request.POST.get('selectedOption')
        print('selected_option', selected_option)
        product_value_qs = ProductOption.objects.get(product__pk=product, option_value__pk=selected_option)
        product_value_id = str(product_value_qs.pk)
        print(quantity_post, selected_option, product_value_id)
        cart = request.session.get('cart')
        print('cart', cart)
        if cart:
            product_value = cart.get(product_value_id)
            print(product_value)
            if product_value:
                cart[product_value_id] += quantity_post
                if cart[product_value_id]+quantity_post <= cart[product_value_id]:
                    cart[product_value_id].pop(selected_option)
            else:
                cart[product_value_id] = quantity_post
        else:
            cart[product_value_id] = quantity_post
        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('shop:product', product_slug=product_slug)


class CartView(CartMixin, View):

    def get(self, request, products, sum_cart):
        if products:
            return render(request, 'shop/cart.html', {'products': products, 'sum_cart': sum_cart})
        else:
            return render(request, 'shop/cart.html',)

    def post(self, request, products, sum_cart):
        return redirect('shop:order')


class DeleteCartView(View):
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        cart.pop(product)
        request.session['cart'] = cart
        return redirect('shop:cart')


class UpdateCartView(View):

    def post(self, request):
        product = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart')
        cart[product] = quantity
        request.session['cart'] = cart
        return redirect('shop:cart')


class OrderView(CartMixin, View):

    def get(self, request, products, sum_cart):
        current_user = request.user
        if products:
            form = OrderForm(initial={'phone_number': current_user.phone_number, 'email': current_user.email})
            return render(request, 'shop/order.html', {'products': products, 'sum_cart': sum_cart, 'form': form})

        else:
            return render(request, 'shop/order.html', )

    def post(self, request, products, sum_cart):
        print(products)
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_order = Order(phone_number=data['phone_number'], email=data['email'],
                              shipping_address=data['shipping_address'], cost_order=sum_cart,
                              customer=request.user)
            order_details = []
            for product, info in products.items():
                print(product, info)
                new_order_detail = OrderDetails(order=new_order, product=product,
                                                quantity=info[0], sum_product=info[1])
                order_details.append(new_order_detail)
            new_order.save()
            OrderDetails.objects.bulk_create(order_details)
            request.session['cart'] = {}

        return redirect('userapp:profile')
