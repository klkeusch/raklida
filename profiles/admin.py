from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('id', 'user', 'description', 'user_rooms')


admin.site.register(Profile, ProfileAdmin)
