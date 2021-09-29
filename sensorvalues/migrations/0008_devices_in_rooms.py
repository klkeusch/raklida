# Generated by Django 3.2.7 on 2021-09-20 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_user_rooms'),
        ('sensorvalues', '0007_alter_devices_assigned_to_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='in_rooms',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
    ]