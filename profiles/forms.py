from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from sensorvalues.models import DeviceUserAssignment


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
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, max_length=300, required=False, label="Informationen")
    user_rooms = forms.CharField(max_length=300, required=False, label="Büro/Räume")
    image = forms.ImageField(label="Profilbild")

    class Meta:
        model = Profile
        fields = ['description', 'user_rooms', 'image']


class DeviceChoiceField(forms.Form):
    devices = forms.ModelChoiceField(queryset=None, label="", empty_label="Bitte Gerät auswählen...")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['devices'].queryset = DeviceUserAssignment.objects.filter(
                device__profile__user=user
            ).values_list(
                "device__profile__assigned_devices__display_name",
                flat=True
            ).distinct()


class UserChoiceField(forms.Form):
    users = forms.ModelChoiceField(queryset=None, label="", empty_label="Bitte Benutzer auswählen...")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['devices'].queryset = DeviceUserAssignment.objects.filter(
                device__profile__user=user
            ).values_list(
                "device__profile__assigned_devices__display_name",
                flat=True
            ).distinct()
