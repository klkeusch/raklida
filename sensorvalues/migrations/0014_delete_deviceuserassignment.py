# Generated by Django 3.2.7 on 2021-10-01 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensorvalues', '0013_devices_assigned_to_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeviceUserAssignment',
        ),
    ]