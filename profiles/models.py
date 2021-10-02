from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sensorvalues.models import DeviceUserAssignment, Devices


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Benutzer")
    image = models.ImageField(default="default.jpg", upload_to="profile_pictures", verbose_name="Profilbild")
    description = models.CharField(max_length=300, blank=True, verbose_name="Kurzbeschreibung")
    user_rooms = models.CharField(max_length=50, blank=True, verbose_name="Raum")
    assigned_devices = models.ManyToManyField('sensorvalues.Devices', through='sensorvalues.DeviceUserAssignment')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def get_assigned_devices(self):
        return ", \n".join([d.display_name for d in self.assigned_devices.all()])

    # @classmethod
    # def get_assigned_devices(d):
    #     return ", \n".join([d.display_name for d in Profile.assigned_devices.all()])

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
