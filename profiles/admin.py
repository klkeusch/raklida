from django.contrib import admin
from .models import Profile
from sensorvalues.models import DeviceUserAssignment
from django import forms


# class DevicesInline(admin.StackedInline):
#     model = Devices
#     extra = 0
#     # raw_id_fields = ('in_rooms',)
#     verbose_name = 'Zugewiesenes Gerät'
#     verbose_name_plural = 'Zugewiesene Geräte'
#     # fk_name = 'in_rooms'
#     show_change_link = True

class DevicesInline(admin.StackedInline):
    model = DeviceUserAssignment
    extra = 0
    # raw_id_fields = ('in_rooms',)
    verbose_name = 'Zugewiesenes Gerät'
    verbose_name_plural = 'Zugewiesene Geräte'
    # fk_name = 'in_rooms'
    show_change_link = True


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    # form = ProfileAdminForm
    list_display = ('id', 'user', 'description', 'user_rooms', 'get_assigned_devices',)
    search_fields = ('assigned_user', 'device',)
    list_display_links = list_display
    # autocomplete_fields = ['user',]
    # list_display_links = ('id', 'user')
    # list_editable = ('description',)
    inlines = [
        DevicesInline,
    ]
    Profile.get_assigned_devices.short_description = 'Zugeordnete Geräte'


admin.site.register(Profile, ProfileAdmin)
