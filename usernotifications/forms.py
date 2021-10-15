from django import forms
from django.contrib.auth.models import User
from .models import Message
from sensorvalues.models import DeviceUserAssignment
from bootstrap_datepicker_plus import DateTimePickerInput


class MessageCreateForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=None, initial=0, label="Empfänger")
    content = forms.CharField(widget=forms.Textarea, max_length=500, required=True, label="Ihre Nachricht")
    incident_date = forms.DateTimeField(label="Zwischenfall-Datum")
    user_devices = forms.ModelChoiceField(
        queryset=None)  # forms.ModelMultipleChoiceField(queryset=None, label="Betroffenes Gerät")#(queryset=Devices.objects.all(), initial=0, label="Betroffenes Gerät")

    class Meta:
        model = Message
        fields = ['recipient', 'content', 'incident_date', 'user_devices']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(MessageCreateForm, self).__init__(*args, **kwargs)

        self.fields['recipient'].queryset = User.objects.all().exclude(
            is_staff=False)  # Benutzer ist niemals Mitarbeiter
        self.fields['incident_date'].widget = DateTimePickerInput(options={
            "format": "DD.MM.YYYY HH:mm",
            "locale": "de",
        }, )
        self.fields['user_devices'].queryset = DeviceUserAssignment.objects.filter(
            device__profile__user=self.request.user
        ).values_list(
            "device__profile__assigned_devices__display_name",
            flat=True
        ).distinct()


class MessageUpdateForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), initial=0, label="Empfänger")
    content = forms.CharField(widget=forms.Textarea, max_length=500, required=True, label="Ihre Nachricht")
    incident_date = forms.DateTimeField(label="Zwischenfall-Datum")

    class Meta:
        model = Message
        fields = ['recipient', 'content', 'incident_date', 'user_devices']
