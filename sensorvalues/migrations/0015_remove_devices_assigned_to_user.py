# Generated by Django 3.2.7 on 2021-10-01 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensorvalues', '0014_delete_deviceuserassignment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devices',
            name='assigned_to_user',
        ),
    ]