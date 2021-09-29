from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Data, Datapoints, Devices, MqttTreeNodes, TreeDatapointTranslations, DevicesTable, DailyAverages, \
    DeviceUserAssignment
from related_admin import RelatedFieldAdmin, getter_for_related_field


# admin.site.register(Datapoints)
admin.site.register(MqttTreeNodes)
admin.site.register(TreeDatapointTranslations)
admin.site.register(DailyAverages)


class DevicesAdmin(admin.ModelAdmin):
    model = Devices
    list_display = ('id', 'display_name', 'location', 'last_status_update', 'in_rooms')


# class DevicesAdmin(RelatedFieldAdmin):
#     # model = Devices
#     list_display = ('id', 'display_name', 'location', 'last_status_update', 'in_rooms', 'assigned_to_user')


class DevicesUserAssignmentAdmin(admin.ModelAdmin):
    model = DeviceUserAssignment
    list_display = ('id', 'user', 'device',)


class DataAdmin(admin.ModelAdmin):
    model = Data
    list_display = ('id', 'timestamp', 'datapoint', 'value_double', 'value_integer', 'value_string', 'is_valid',)
    list_filter = ['timestamp']


class DatapointAdmin(admin.ModelAdmin):
    model = Datapoints
    list_display = (
        'id', 'display_name', 'unit', 'device', 'current_value_double', 'current_value_integer', 'current_value_string',
        'last_update', 'store_historic_data')


admin.site.register(Devices, DevicesAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(DeviceUserAssignment, DevicesUserAssignmentAdmin)
admin.site.register(Datapoints, DatapointAdmin)
