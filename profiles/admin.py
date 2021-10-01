from django.contrib import admin
from .models import Profile
from sensorvalues.models import Devices


class DevicesInline(admin.TabularInline):
    model = Devices
    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('id', 'user', 'description', 'user_rooms',)
    list_display_links = ('id', 'user')
    inlines = [
        DevicesInline,
    ]

admin.site.register(Profile, ProfileAdmin)
