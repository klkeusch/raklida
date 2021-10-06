# Generated by Django 3.2.7 on 2021-10-06 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_profile_assigned_devices'),
        ('sensorvalues', '0017_auto_20211002_0750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='treedatapointtranslations',
            options={'get_latest_by': ['-timestamp'], 'verbose_name': 'MQTT-Tree-Datapoint-Verknüpfung', 'verbose_name_plural': 'MQTT-Tree-Datapoint-Verknüpfungen'},
        ),
        migrations.AlterField(
            model_name='datapoints',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='deviceuserassignment',
            name='assigned_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.profile', verbose_name='Benutzer'),
        ),
        migrations.AlterField(
            model_name='deviceuserassignment',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sensorvalues.devices', verbose_name='Gerät'),
        ),
        migrations.AlterField(
            model_name='deviceuserassignment',
            name='end_date',
            field=models.DateField(verbose_name='Enddatum'),
        ),
        migrations.AlterField(
            model_name='deviceuserassignment',
            name='start_date',
            field=models.DateField(verbose_name='Startdatum'),
        ),
        migrations.AlterField(
            model_name='deviceuserassignment',
            name='usage_reason',
            field=models.CharField(max_length=100, verbose_name='Nutzungsgrund/Details'),
        ),
    ]
