# Generated by Django 3.2.7 on 2021-09-20 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensorvalues', '0009_auto_20210920_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='data',
            options={'managed': True, 'verbose_name': 'Messdaten-Eintrag', 'verbose_name_plural': 'Messdaten-Einträge'},
        ),
    ]
