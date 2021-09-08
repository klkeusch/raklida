from django.contrib import admin
from .models import Data, Datapoints, Devices

admin.site.register(Data)
admin.site.register(Datapoints)
admin.site.register(Devices)
