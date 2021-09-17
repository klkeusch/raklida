from django.shortcuts import render
from usernotifications.apps import Inbox
from .models import Message
from .services import MessagingService
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Message


def sending(request):
    send = MessagingService.send_message()
    return render(request, "usernotifications/message_list.html", context={'send': send})


class MessageListView(generic.ListView):
    model = Message
    ordering = ['-sent_at']
    paginate_by = 5
