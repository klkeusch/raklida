from django.contrib import admin
from .models import Profile
from sensorvalues.models import Devices


class DevicesInline(admin.StackedInline):
    model = Devices
    extra = 0
    # raw_id_fields = ('in_rooms',)
    verbose_name = 'Zugewiesenes Gerät'
    verbose_name_plural = 'Zugewiesene Geräte'
    fk_name = 'in_rooms'
    show_change_link = True


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('id', 'user', 'description', 'user_rooms',)
    list_display_links = ('id', 'user')
    inlines = [
        DevicesInline,
    ]

admin.site.register(Profile, ProfileAdmin)
