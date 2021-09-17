from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sensorvalues.models import Devices


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Benutzer")
    image = models.ImageField(default="default.jpg", upload_to="profile_pictures", verbose_name="Profilbild")
    description = models.CharField(max_length=300, blank=True, verbose_name="Kurzbeschreibung")
    # ass_device = models.ManyToManyField(Devices) -- ersetzen mit eigener table in sensorvalues

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
