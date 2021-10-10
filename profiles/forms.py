from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from sensorvalues.models import Devices, DeviceUserAssignment


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
    user_rooms = forms.CharField(max_length=300, required=False, label="Büro/Räume")
    image = forms.ImageField(label="Profilbild")

    class Meta:
        model = Profile
        fields = ['description', 'user_rooms', 'image']


# def devices_assigned_to_user(request):
#     if request is None:
#         return DeviceUserAssignment.objects.none()
#
#     device_user = request.user
#     return DeviceUserAssignment.objects.filter(assigned_user=device_user)


# class DeviceChoiceField(forms.Form):
#     devices = forms.ModelChoiceField(
#         # queryset=Devices.objects.values_list("display_name", flat=True).distinct(),  # .values_list("field von model", flat=True).distinct()
#         # queryset=DeviceUserAssignment.objects.values_list("device__display_name", flat=True).distinct(),
#         queryset=DeviceUserAssignment.objects.values_list("device__profile__assigned_devices", flat=True).distinct(),
#         # queryset=devices_assigned_to_user,
#         empty_label="Bitte Gerät auswählen",
#         to_field_name="device",
#     )

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
            ).distinct(

            )
