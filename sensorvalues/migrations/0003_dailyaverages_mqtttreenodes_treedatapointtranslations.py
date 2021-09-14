# Generated by Django 3.2.7 on 2021-09-14 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensorvalues', '0002_datapoints_devices'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyAverages',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('value_night', models.FloatField(blank=True, null=True)),
                ('value_day', models.FloatField(blank=True, null=True)),
                ('value_min', models.FloatField(blank=True, null=True)),
                ('value_max', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'daily_averages',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MqttTreeNodes',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('is_leaf', models.BooleanField()),
                ('parent_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'mqtt_tree_nodes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TreeDatapointTranslations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'tree_datapoint_translations',
                'managed': False,
            },
        ),
    ]