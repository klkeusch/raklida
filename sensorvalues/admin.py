from django.contrib import admin
from .models import Data, Datapoints, Devices, MqttTreeNodes, TreeDatapointTranslations, DevicesTable, DailyAverages

admin.site.register(Data)
admin.site.register(Datapoints)
admin.site.register(Devices)
admin.site.register(MqttTreeNodes)
admin.site.register(TreeDatapointTranslations)
admin.site.register(DailyAverages)

