from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'userapp'
urlpatterns = [
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('login/',
         auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="userapp/login.html"),
         name='login'),
    path('logout/', logout_user, name='logout'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('register/', RegisterView.as_view(), name='register'),
]
