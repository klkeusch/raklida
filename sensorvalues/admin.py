from django.contrib import admin
from .models import Data, Datapoints, Devices, MqttTreeNodes, TreeDatapointTranslations, DevicesTable, DailyAverages

admin.site.register(Datapoints)
admin.site.register(MqttTreeNodes)
admin.site.register(TreeDatapointTranslations)
admin.site.register(DailyAverages)


class DevicesAdmin(admin.ModelAdmin):
    model = Devices
    list_display = ('id', 'display_name', 'location', 'last_status_update',)


#class DevicesUserAssignmentAdmin(admin.ModelAdmin):
#    model = DeviceUserAssignment
#    list_display = ('id', 'user', 'device',)


class DataAdmin(admin.ModelAdmin):
    model = Data
    list_display = ('id', 'timestamp', 'value_double', 'value_integer', 'value_string', 'is_valid',)


admin.site.register(Devices, DevicesAdmin)
admin.site.register(Data, DataAdmin)
#admin.site.register(DeviceUserAssignment, DevicesUserAssignmentAdmin)
