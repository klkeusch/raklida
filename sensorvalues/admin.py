from django.contrib import admin
# Info: Django Dropdown Filter tauchen erst ab >4 Einträgen auf
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from .models import Data, Datapoints, Devices, MqttTreeNodes, TreeDatapointTranslations, DailyAverages, \
    DeviceUserAssignment

admin.site.register(DailyAverages)


class TreeDatapointTranslationsAdmin(admin.ModelAdmin):
    model = TreeDatapointTranslations
    sortable_by = ('datapoint', 'mqtt_node', 'id')
    list_display = ('id', 'datapoint', 'mqtt_node',)
    list_display_links = ('id', 'datapoint')
    list_filter = (
        ('datapoint__display_name', DropdownFilter),
        ('mqtt_node__name', DropdownFilter),
    )


class MqttTreeNodesAdmin(admin.ModelAdmin):
    model = MqttTreeNodes
    sortable_by = ('parent_id', 'is_leaf', 'name', 'id')
    list_display = ('id', 'name', 'parent_id', 'is_leaf',)
    list_display_links = ('id', 'name',)
    list_filter = (
        ('name', DropdownFilter),
        ('is_leaf', DropdownFilter),
        ('parent_id', DropdownFilter),
    )


class DevicesAdmin(admin.ModelAdmin):
    model = Devices
    list_display = ('id', 'display_name', 'location', 'last_status_update',)
    list_display_links = ('id', 'display_name')
    list_filter = (
        ('location', DropdownFilter),
        ('deviceuserassignment__assigned_user__user__username', DropdownFilter),
    )


class DevicesUserAssignmentAdmin(admin.ModelAdmin):
    model = DeviceUserAssignment
    fields = ['assigned_user', 'device', 'usage_reason', ('start_date', 'end_date')]
    list_display = ('id', 'assigned_user', 'device', 'usage_reason', 'start_date', 'end_date',)
    list_display_links = ('id', 'assigned_user', 'device')
    list_filter = (
        ('assigned_user', RelatedDropdownFilter),
        ('device', RelatedDropdownFilter),
        # Dates not implemented yet
        # 'start_date',
        # 'end_date',
    )


class DataAdmin(admin.ModelAdmin):
    model = Data
    list_display_links = ['id', 'timestamp', 'datapoint']
    list_display = ('id', 'timestamp', 'datapoint', 'value_double', 'value_integer', 'value_string', 'is_valid')
    list_filter = (
        'timestamp',
        ('datapoint__device__display_name', DropdownFilter),
        ('datapoint__device__deviceuserassignment__assigned_user', RelatedDropdownFilter),
        ('datapoint__name', DropdownFilter),
    )


class DatapointAdmin(admin.ModelAdmin):
    model = Datapoints
    list_filter = (
        ('device', RelatedDropdownFilter),
        ('device__deviceuserassignment__assigned_user', RelatedDropdownFilter),
        ('name', DropdownFilter)
    )
    list_display = (
        'id', 'name', 'display_name', 'unit', 'device', 'current_value_double', 'current_value_integer',
        'current_value_string',
        'last_update', 'store_historic_data')
    list_display_links = ('id', 'name', 'display_name')


admin.site.register(Devices, DevicesAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(DeviceUserAssignment, DevicesUserAssignmentAdmin)
admin.site.register(Datapoints, DatapointAdmin)
admin.site.register(MqttTreeNodes, MqttTreeNodesAdmin)
admin.site.register(TreeDatapointTranslations, TreeDatapointTranslationsAdmin)
