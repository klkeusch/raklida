from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pictures")
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.user.username}\'s Profil...'
