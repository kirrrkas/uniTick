from shop.models import ProductOption


class DataMixin:

    def dispatch(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        return super().dispatch(request, *args, **kwargs)


class CartMixin:

    def dispatch(self, request, *args, **kwargs):
        products_session = request.session.get('cart')
        if products_session:
            products = {}
            sum_cart = 0
            for product_value, quantity in products_session.items():
                product_value_qs = ProductOption.objects.get(pk=product_value)
                price = product_value_qs.product.price
                products[product_value_qs] = [quantity, quantity * price]

                sum_cart += quantity * price

            kwargs.update({'products': products, 'sum_cart': sum_cart})
        else:
            kwargs.update({'products': None, 'sum_cart': None})
        return super().dispatch(request, *args, **kwargs)
