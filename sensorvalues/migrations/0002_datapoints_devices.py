# Generated by Django 3.2.7 on 2021-09-08 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensorvalues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datapoints',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('unit', models.CharField(max_length=15)),
                ('display_name', models.CharField(max_length=50)),
                ('store_historic_data', models.BooleanField()),
                ('device_sub_id', models.BigIntegerField()),
                ('current_value_double', models.FloatField(blank=True, null=True)),
                ('current_value_integer', models.BigIntegerField(blank=True, null=True)),
                ('current_value_string', models.CharField(blank=True, max_length=30, null=True)),
                ('last_update', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'datapoints',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=30)),
                ('current_status_code', models.BigIntegerField()),
                ('last_status_update', models.TimeField()),
                ('device_type', models.CharField(blank=True, max_length=30, null=True)),
                ('display_name', models.CharField(max_length=50)),
                ('platform', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'devices',
                'managed': False,
            },
        ),
    ]
