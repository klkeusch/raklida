# Generated by Django 3.2.7 on 2021-10-24 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensorvalues', '0020_alter_data_options'),
        ('profiles', '0005_profile_assigned_devices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='assigned_devices',
            field=models.ManyToManyField(through='sensorvalues.DeviceUserAssignment', to='sensorvalues.Devices', verbose_name='Zugeordnete Geräte'),
        ),
    ]
