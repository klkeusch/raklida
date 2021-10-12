from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinLengthValidator

content_validator = MinLengthValidator(limit_value=50, message="Der Bloginhalt sollte mindestens 50 Zeichen enthalten!")


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name="Titel")
    content = models.TextField(validators=[content_validator], verbose_name="Inhalt")
    date_published = models.DateTimeField(default=timezone.now, verbose_name="Veröffentlichungsdatum")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")

    class Meta:
        verbose_name = 'Blogeintrag'
        verbose_name_plural = 'Blogeinträge'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={'pk': self.pk})
