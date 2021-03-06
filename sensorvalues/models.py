"""Database models for sensorvalues app"""
from django.db import models
from django.contrib.auth.models import User
import django_tables2 as tables


class Data(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    timestamp = models.DateTimeField(verbose_name="Zeitstempel")
    value_double = models.FloatField(blank=True, null=True, verbose_name="Double-Wert")
    value_integer = models.BigIntegerField(blank=True, null=True, verbose_name="Integer-Wert")
    value_string = models.CharField(max_length=100, blank=True, null=True, verbose_name="Statuscode")
    datapoint = models.ForeignKey('Datapoints', on_delete=models.CASCADE, verbose_name="Datenpunkt", blank=True,
                                  null=True)
    is_valid = models.BooleanField(verbose_name="Gültig?")

    class Meta:
        managed = True
        verbose_name = 'Messwert'
        verbose_name_plural = 'Messwerte'
        get_latest_by = ['-timestamp']

    def __str__(self):
        return str(self.datapoint)


class Devices(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    location = models.CharField(max_length=30, verbose_name="Standort")
    current_status_code = models.BigIntegerField(verbose_name="Aktueller Statuscode")
    last_status_update = models.TimeField(verbose_name="Letzter Statuscode")
    device_type = models.CharField(max_length=30, blank=True, null=True, verbose_name="Gerätetyp")
    display_name = models.CharField(max_length=50, verbose_name="Anzeigename")
    platform = models.CharField(max_length=30, blank=True, null=True, verbose_name="Geräte-Plattform")
    mac_address = models.CharField(max_length=20, blank=True, null=True, verbose_name="MAC-Adresse")

    class Meta:
        verbose_name = 'Gerät'
        verbose_name_plural = 'Geräte'

    def __str__(self):
        return self.display_name


class DeviceUserAssignment(models.Model):
    device = models.ForeignKey('sensorvalues.Devices', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="Gerät")
    assigned_user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name="Benutzer")
    usage_reason = models.CharField(max_length=100, verbose_name="Nutzungsgrund/Details")
    start_date = models.DateField(verbose_name="Startdatum")
    end_date = models.DateField(verbose_name="Enddatum")

    def __str__(self):
        return f'{self.device.display_name} (Nutzer: {self.assigned_user.user.username})'

    class Meta:
        verbose_name = 'Benutzer-Gerät-Zuordnung'
        verbose_name_plural = 'Benutzer-Gerät-Zuordnungen'


class Datapoints(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=50, verbose_name="Name")
    unit = models.CharField(max_length=15, verbose_name="Einheit")
    display_name = models.CharField(max_length=50, verbose_name="Anzeigename")
    store_historic_data = models.BooleanField(verbose_name="Messwertaufzeichnung?")
    device_sub_id = models.BigIntegerField(verbose_name="Geräte-Sub-ID")
    device = models.ForeignKey(Devices, on_delete=models.CASCADE, verbose_name="Gerät", null=True, blank=True)
    current_value_double = models.FloatField(blank=True, null=True, verbose_name="Aktueller Double-Wert")
    current_value_integer = models.BigIntegerField(blank=True, null=True, verbose_name="Aktueller Integer-Wert")
    current_value_string = models.CharField(max_length=30, blank=True, null=True, verbose_name="Aktueller Statuscode")
    last_update = models.DateTimeField(blank=True, null=True, verbose_name="Letztes Update")

    class Meta:
        verbose_name = 'Datenpunkt'
        verbose_name_plural = 'Datenpunkte'
        get_latest_by = ['-last_update']

    def __str__(self):
        return self.display_name


class DailyAverages(models.Model):
    id = models.BigAutoField(primary_key=True)
    datapoint_id = models.ForeignKey(Datapoints, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    value_night = models.FloatField(blank=True, null=True)
    value_day = models.FloatField(blank=True, null=True)
    value_min = models.FloatField(blank=True, null=True)
    value_max = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Tagesdurchschnitt'
        verbose_name_plural = 'Tagesdurchschnitte'


class MqttTreeNodes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Name")
    is_leaf = models.BooleanField(verbose_name="Ist Blatt?")
    parent_id = models.BigIntegerField(verbose_name="Eltern-ID")

    class Meta:
        verbose_name = 'MQTT-Tree-Node'
        verbose_name_plural = 'MQTT-Tree-Nodes'

    def __str__(self):
        return self.name


class TreeDatapointTranslations(models.Model):
    id = models.BigAutoField(primary_key=True)
    datapoint = models.ForeignKey(Datapoints, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name="Datenpunkt")
    mqtt_node = models.ForeignKey(MqttTreeNodes, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name="MQTT-Node")

    class Meta:
        verbose_name = 'MQTT-Tree-Datapoint-Verknüpfung'
        verbose_name_plural = 'MQTT-Tree-Datapoint-Verknüpfungen'

    def __str__(self):
        return f"{self.datapoint} ({self.datapoint.device})"


class DevicesTable(tables.Table):
    class Meta:
        model = Devices
