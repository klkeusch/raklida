# Generated by Django 3.2.7 on 2021-09-20 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usernotifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='incident_data',
            field=models.DateTimeField(blank=True, null=True, verbose_name='incident date'),
        ),
    ]