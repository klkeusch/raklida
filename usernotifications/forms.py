from django import forms
from django.contrib.auth.models import User
from .models import Message


class MessageCreateForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), initial=0, label="Empfänger")
    content = forms.CharField(widget=forms.Textarea, max_length=500, required=True, label="Ihre Nachricht")
    # sent_at = forms.DateTimeField(label="Datum des Zwischenfalls")
    incident_date = forms.DateTimeField(label="Zwischenfall-Datum")

    class Meta:
        model = Message
        fields = ['recipient', 'content', 'incident_date']


class MessageUpdateForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), initial=0, label="Empfänger")
    content = forms.CharField(widget=forms.Textarea, max_length=500, required=True, label="Ihre Nachricht")
    # sent_at = forms.DateTimeField(label="Datum des Zwischenfalls")
    incident_date = forms.DateTimeField(label="Zwischenfall-Datum")

    class Meta:
        model = Message
        fields = ['recipient', 'content', 'incident_date']
