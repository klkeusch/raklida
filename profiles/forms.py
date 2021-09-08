from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="Vorname")
    last_name = forms.CharField(max_length=50, required=True, label="Nachname")
    email = forms.EmailField(required=True, label="E-Mail-Adresse")

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="E-Mail-Adresse")
    first_name = forms.CharField(max_length=50, required=True, label="Vorname")
    last_name = forms.CharField(max_length=50, required=True, label="Nachname")

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, max_length=300, required=False, label="Informationen")
    image = forms.ImageField(label="Profilbild")

    class Meta:
        model = Profile
        fields = ['description', 'image']
