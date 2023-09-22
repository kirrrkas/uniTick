from django import forms
from shop.models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['phone_number', 'email', 'shipping_address']
