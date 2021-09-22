from django.apps import AppConfig
from django import VERSION as DJANGO_VERSION

Inbox = None

if DJANGO_VERSION >= (1, 7):
    from django.apps import AppConfig


    class UsernotificationsConfig(AppConfig):
        name = 'usernotifications'
        label = 'usernotifications'
        verbose_name="Benutzermeldungen"

        def ready(self):
            # For convenience
            from usernotifications.services import MessagingService
            global Inbox
            Inbox = MessagingService()

else:
    def populateInbox():
        from usernotifications.services import MessagingService
        global Inbox
        Inbox = MessagingService()
