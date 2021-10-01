from django.contrib import admin
from .models import Profile
from sensorvalues.models import Devices
from django import forms


class DevicesInline(admin.StackedInline):
    model = Devices
    extra = 0
    # raw_id_fields = ('in_rooms',)
    verbose_name = 'Zugewiesenes Gerät'
    verbose_name_plural = 'Zugewiesene Geräte'
    fk_name = 'in_rooms'
    show_change_link = True


# class ProfileAdminForm(forms.ModelForm): # zum vergroessern des Description Fields in django-admin
#     description = forms.CharField(widget=forms.Textarea)
#
#     class Meta:
#         model = Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    # form = ProfileAdminForm
    list_display = ('id', 'user', 'description', 'user_rooms',)
    list_display_links = ('id', 'user')
    # list_editable = ('description',)
    inlines = [
        DevicesInline,
    ]


admin.site.register(Profile, ProfileAdmin)
