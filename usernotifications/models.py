from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from sensorvalues.models import DeviceUserAssignment

# AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Message(models.Model):
    """
    A private directmessage
    """
    content = models.TextField(_('Content'))
    # sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_dm', verbose_name=_("Sender"), on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_dm', verbose_name=_("Sender"),
                               on_delete=models.CASCADE)
    #recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_dm', verbose_name=_("Recipient"), on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_dm', verbose_name=_("Recipient"), on_delete=models.CASCADE)
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Gesendet")
    # sent_at = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))    _("sent at") _("read at"),
    read_at = models.DateTimeField( null=True, blank=True, verbose_name="Gelesen")
    incident_date = models.DateTimeField(verbose_name="Vorfalldatum", null=True, blank=True)
    user_devices = models.ForeignKey(DeviceUserAssignment, on_delete=models.CASCADE, verbose_name="Betroffene Geräte", null=True)

    class Meta:
        verbose_name = 'Benutzermeldung'
        verbose_name_plural = 'Benutzermeldungen'

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={'pk': self.pk})

    @property
    def unread(self):
        """returns whether the message was read or not"""
        if self.read_at is not None:
            return False
        return True

    def __str__(self):
        return self.content

    def save(self, **kwargs):
        if self.sender == self.recipient:
            raise ValidationError("You can't send messages to yourself")

        if not self.id:
            self.sent_at = timezone.now()
            #self.incident_date = timezone.now()
        super(Message, self).save(**kwargs)
