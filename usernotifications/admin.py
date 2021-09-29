from .models import Message
from django.contrib import admin
from related_admin import RelatedFieldAdmin, getter_for_related_field


# class MessageAdmin(admin.ModelAdmin):
#     model = Message
#     list_display = ('id', 'sent_at', 'sender', 'content', 'incident_date',)
#     list_filter = ['sent_at', 'incident_date']

class MessageAdmin(RelatedFieldAdmin):
    # model = Message
    list_display = ('id', 'sent_at', 'sender', 'content', 'incident_date')
    list_filter = ['sent_at', 'incident_date']


admin.site.register(Message, MessageAdmin)
