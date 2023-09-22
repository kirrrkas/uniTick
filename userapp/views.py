from collections import defaultdict
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from shop.models import OrderDetails
from userapp.forms import ProfileForm, RegisterForm
from userapp.models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление, в котором отображается форма для редактирования профиля пользователя.

    Использует форму, динамически созданную для модели "Профиль",
    и шаблон обновления модели по умолчанию.
    """
    model = User
    context_object_name = 'user'
    form_class = ProfileForm
    template_name = 'userapp/profile.html'
    success_url = reverse_lazy('userapp:profile')
    # fields = ['email', 'phone_number', 'last_name', 'first_name']

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        tickets = obj.ticket_set.all()
        context['tickets'] = tickets
        orders_details = OrderDetails.objects.filter(order__customer=obj)#.order_by('order', 'order__pk')

        orders = defaultdict(list)
        for result in orders_details:
            orders[result.order].append(result)

        context['orders'] = dict(orders)

        return context


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    Изменение пароля пользователя
    """
    template_name = 'userapp/user_password_change.html'
    success_message = 'Ваш пароль был успешно изменён!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('userapp:login')


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('userapp:login')
    template_name = 'userapp/register.html'
