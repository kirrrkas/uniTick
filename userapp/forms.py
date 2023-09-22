from django import forms
# from django.contrib.auth.forms import AuthenticationForm
from userapp.models import User
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'last_name', 'first_name', 'middle_name']


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'email',
            'phone_number',
            'first_name',
            'middle_name',
            'last_name',
            'password1',
            'password2',
            ]
