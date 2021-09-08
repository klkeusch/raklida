from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="Vorname")
    last_name = forms.CharField(max_length=50, required=True, label="Nachname")
    email = forms.EmailField(required=True, label="E-Mail-Adresse")

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
