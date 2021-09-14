from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sensorvalues.models import Devices


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pictures")
    description = models.CharField(max_length=300, blank=True)
    ass_device = models.ManyToManyField(Devices)

    def __str__(self):
        # return f'{self.user.username}\'s Profil...'
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
