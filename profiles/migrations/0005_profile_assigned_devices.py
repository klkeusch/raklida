# Generated by Django 3.2.7 on 2021-10-02 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensorvalues', '0017_auto_20211002_0750'),
        ('profiles', '0004_profile_user_rooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='assigned_devices',
            field=models.ManyToManyField(through='sensorvalues.DeviceUserAssignment', to='sensorvalues.Devices'),
        ),
    ]