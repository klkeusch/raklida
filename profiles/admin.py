from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from .models import Profile
from sensorvalues.models import DeviceUserAssignment


class DevicesInline(admin.StackedInline):
    model = DeviceUserAssignment
    extra = 0
    verbose_name = 'Zugewiesenes Gerät'
    verbose_name_plural = 'Zugewiesene Geräte'
    show_change_link = True


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('id', 'user', 'description', 'user_rooms', 'get_assigned_devices',)
    list_display_links = ('id', 'user')
    list_filter = (
        ('user', RelatedDropdownFilter),
        ('assigned_devices', RelatedDropdownFilter),
    )
    inlines = [
        DevicesInline,
    ]
    Profile.get_assigned_devices.short_description = 'Zugeordnete Geräte'


admin.site.register(Profile, ProfileAdmin)
