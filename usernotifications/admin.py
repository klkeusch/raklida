from .models import Message
from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('id', 'sent_at', 'sender', 'content', 'incident_date',)
    list_filter = (
        'sent_at',
        ('sender', RelatedDropdownFilter),
    )


admin.site.register(Message, MessageAdmin)
