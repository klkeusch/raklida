# Generated by Django 3.2.7 on 2021-10-10 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensorvalues', '0019_auto_20211006_0827'),
        ('usernotifications', '0008_alter_message_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='user_devices',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sensorvalues.deviceuserassignment', verbose_name='Geräte des Benutzers'),
        ),
    ]
