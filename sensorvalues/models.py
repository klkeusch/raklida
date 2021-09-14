from django.db import models
import django_tables2 as tables


class Data(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    timestamp = models.DateTimeField(verbose_name="Zeitstempel")
    value_double = models.FloatField(blank=True, null=True, verbose_name="Double-Wert")
    value_integer = models.BigIntegerField(blank=True, null=True, verbose_name="Integer-Wert")
    value_string = models.CharField(max_length=100, blank=True, null=True, verbose_name="Statuscode")
    datapoint = models.ForeignKey('Datapoints', models.CASCADE, verbose_name="Datenpunkt")
    is_valid = models.BooleanField(verbose_name="Gültig?")

    class Meta:
        managed = False
        db_table = 'data'

    def __str__(self):
        return str(self.datapoint)


class Datapoints(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=30, verbose_name="Name")
    unit = models.CharField(max_length=15, verbose_name="Einheit")
    display_name = models.CharField(max_length=50, verbose_name="Anzeigename")
    store_historic_data = models.BooleanField(verbose_name="Messwertaufzeichnung?")
    device_sub_id = models.BigIntegerField(verbose_name="Geräte-Sub-ID")
    device = models.ForeignKey('Devices', models.DO_NOTHING, verbose_name="Gerät")
    current_value_double = models.FloatField(blank=True, null=True, verbose_name="Aktueller Double-Wert")
    current_value_integer = models.BigIntegerField(blank=True, null=True, verbose_name="Aktueller Integer-Wert")
    current_value_string = models.CharField(max_length=30, blank=True, null=True, verbose_name="Aktueller Statuscode")
    last_update = models.DateTimeField(blank=True, null=True, verbose_name="Letztes Update")

    class Meta:
        managed = False
        db_table = 'datapoints'

    def __str__(self):
        return self.display_name


class DailyAverages(models.Model):
    id = models.BigAutoField(primary_key=True)
    datapoint = models.ForeignKey('Datapoints', models.CASCADE)
    date = models.DateField()
    value_night = models.FloatField(blank=True, null=True)
    value_day = models.FloatField(blank=True, null=True)
    value_min = models.FloatField(blank=True, null=True)
    value_max = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_averages'


class Devices(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    location = models.CharField(max_length=30, verbose_name="Standort")
    current_status_code = models.BigIntegerField(verbose_name="Aktueller Statuscode")
    last_status_update = models.TimeField(verbose_name="Letzter Statuscode")
    device_type = models.CharField(max_length=30, blank=True, null=True, verbose_name="Gerätetyp")
    display_name = models.CharField(max_length=50, verbose_name="Anzeigename")
    platform = models.CharField(max_length=30, blank=True, null=True, verbose_name="Geräte-Plattform")

    class Meta:
        managed = False
        db_table = 'devices'

    def __str__(self):
        return self.display_name


class MqttTreeNodes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_leaf = models.BooleanField()
    parent_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'mqtt_tree_nodes'

    def __str__(self):
        return self.name


class TreeDatapointTranslations(models.Model):
    id = models.BigAutoField(primary_key=True)
    datapoint = models.ForeignKey(Datapoints, models.CASCADE)
    mqtt_node = models.ForeignKey(MqttTreeNodes, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'tree_datapoint_translations'

    def __str__(self):
        return self.datapoint


class DevicesTable(tables.Table):
    # display_name = tables.Column(accessor='datapoint.display_name')

    class Meta:
        model = Devices
