from django.db import models
import django_tables2 as tables


class Data(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    value_double = models.FloatField(blank=True, null=True)
    value_integer = models.BigIntegerField(blank=True, null=True)
    value_string = models.CharField(max_length=100, blank=True, null=True)
    datapoint = models.ForeignKey('Datapoints', models.DO_NOTHING)
    is_valid = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'data'

    def __str__(self):
        return str(self.datapoint)


class Datapoints(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=15)
    display_name = models.CharField(max_length=50)
    store_historic_data = models.BooleanField()
    device_sub_id = models.BigIntegerField()
    device = models.ForeignKey('Devices', models.DO_NOTHING)
    current_value_double = models.FloatField(blank=True, null=True)
    current_value_integer = models.BigIntegerField(blank=True, null=True)
    current_value_string = models.CharField(max_length=30, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datapoints'

    def __str__(self):
        return self.display_name


class Devices(models.Model):
    id = models.BigAutoField(primary_key=True)
    location = models.CharField(max_length=30)
    current_status_code = models.BigIntegerField()
    last_status_update = models.TimeField()
    device_type = models.CharField(max_length=30, blank=True, null=True)
    display_name = models.CharField(max_length=50)
    platform = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devices'

    def __str__(self):
        return self.display_name


class SimpleTable(tables.Table):
    class Meta:
        model = Data
