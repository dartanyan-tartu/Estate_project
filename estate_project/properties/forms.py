from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .forms import RegisterForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )

    username = forms.CharField(
        widget= forms.TextInput(attrs={'class': 'form-input'})
    )

    password1 = forms.CharField(
        label= 'Пароль пользователя',
        widget= forms.PasswordInput(attrs={'class': 'form-input'})
    )

    password2 = forms.CharField(
        label= 'Подтвердите пароль',
        widget= forms.PasswordInput(attrs={'class': 'form-input'})
    )

class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2'] 