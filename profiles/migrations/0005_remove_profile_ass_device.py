# Generated by Django 3.2.7 on 2021-09-16 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_profile_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='ass_device',
        ),
    ]
