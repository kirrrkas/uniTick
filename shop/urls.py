from django.urls import path
from .views import *

app_name = 'shop'
urlpatterns = [
    path('', ProductList.as_view(), name='home'),
    path('product/<slug:product_slug>', ShowProduct.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('delete/', DeleteCartView.as_view(), name='delete'),
    path('update/', UpdateCartView.as_view(), name='update'),
    path('order/', OrderView.as_view(), name='order'),
]
