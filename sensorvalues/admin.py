from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Data, Datapoints, Devices, MqttTreeNodes, TreeDatapointTranslations, DevicesTable, DailyAverages, DeviceUserAssignment
from related_admin import RelatedFieldAdmin, getter_for_related_field


# admin.site.register(Datapoints)
# admin.site.register(MqttTreeNodes)
# admin.site.register(TreeDatapointTranslations)
admin.site.register(DailyAverages)


class TreeDatapointTranslationsAdmin(admin.ModelAdmin):
    model = TreeDatapointTranslations
    sortable_by = ('datapoint', 'mqtt_node',)
    list_filter = ('datapoint', 'mqtt_node',)
    list_display = ('id', 'datapoint', 'mqtt_node',)
    list_display_links = list_display


class MqttTreeNodesAdmin(admin.ModelAdmin):
    model = MqttTreeNodes
    sortable_by = ('parent_id', 'is_leaf',)
    list_filter = ('name', 'is_leaf', 'parent_id',)
    list_display = ('id', 'name', 'parent_id', 'is_leaf',)
    list_display_links = ('id', 'name',)


class DevicesAdmin(admin.ModelAdmin):
    model = Devices
    # list_display = ('id', 'display_name', 'location', 'last_status_update', 'in_rooms')
    list_display = ('id', 'display_name', 'location', 'last_status_update',)
    list_display_links = ('id', 'display_name')
    # list_filter = ('in_rooms', 'location',)
    list_filter = ('location',)
    search_fields = ('assigned_user', 'device',)

# class DevicesAdmin(RelatedFieldAdmin):
#     # model = Devices
#     list_display = ('id', 'display_name', 'location', 'last_status_update', 'in_rooms', 'assigned_to_user')


class DevicesUserAssignmentAdmin(admin.ModelAdmin):
    model = DeviceUserAssignment
    fields = ['assigned_user', 'device', 'usage_reason', ('start_date', 'end_date')]
    list_display = ('id', 'assigned_user', 'device', 'usage_reason', 'start_date', 'end_date',)
    list_display_links = list_display
    list_filter = ['assigned_user']
    # search_fields = ('assigned_user', 'device',)
    # autocomplete_fields = ['assigned_user', 'device',]


class DataAdmin(admin.ModelAdmin):
    model = Data
    list_display = ('id', 'timestamp', 'datapoint', 'value_double', 'value_integer', 'value_string', 'is_valid',)
    list_filter = ['timestamp', 'datapoint',]


class DatapointAdmin(admin.ModelAdmin):
    model = Datapoints
    list_filter = ['device',]
    list_display = (
        'id', 'display_name', 'unit', 'device', 'current_value_double', 'current_value_integer', 'current_value_string',
        'last_update', 'store_historic_data')
    list_display_links = list_display


admin.site.register(Devices, DevicesAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(DeviceUserAssignment, DevicesUserAssignmentAdmin)
admin.site.register(Datapoints, DatapointAdmin)
admin.site.register(MqttTreeNodes, MqttTreeNodesAdmin)
admin.site.register(TreeDatapointTranslations, TreeDatapointTranslationsAdmin)