from django.contrib import admin
from .models import Profile


# admin.site.register(Profile)


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('id', 'user', 'description',)


admin.site.register(Profile, ProfileAdmin)
