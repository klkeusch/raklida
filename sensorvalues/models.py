from django.db import models
import django_tables2 as tables


class Data(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    value_double = models.FloatField(blank=True, null=True)
    value_integer = models.BigIntegerField(blank=True, null=True)
    value_string = models.CharField(max_length=100, blank=True, null=True)
    # datapoint = models.ForeignKey('Datapoints', models.DO_NOTHING)
    is_valid = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'data'

    def __str__(self):
        return self.id


class SimpleTable(tables.Table):
    class Meta:
        model = Data
