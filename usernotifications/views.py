from django.shortcuts import render, redirect
from usernotifications.apps import Inbox
from .services import MessagingService
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Message
from .forms import MessageCreateForm, MessageUpdateForm
from django.contrib.auth.models import User


# def sending(request):
#     send = MessagingService.send_message()
#     return render(request, "usernotifications/message_list.html", context={'send': send})


class MessageListView(generic.ListView):
    model = Message

    # ordering = ['-sent_at']
    # paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        # return Message.objects.filter(sender=self.kwargs['pk'])
        return Message.objects.filter(sender=self.request.user)


class MessageCreateView(generic.CreateView):
    model = Message
    # fields = ['recipient', 'content', 'sent_at']
    form_class = MessageCreateForm
    success_url = "/user-dashboard/"
    success_message = "Nachricht erfolgreich erstellt!"

    def get_form(self):
        form = super().get_form()
        form.fields['incident_date'].widget = DateTimePickerInput(options={
            "format": "DD.MM.YYYY HH:mm",
            "locale": "de",
        }, )
        return form

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


class MessageDetailView(generic.DetailView):
    model = Message


class MessageUpdateView(generic.UpdateView):
    model = Message
    form_class = MessageUpdateForm
    # fields = ['content', 'sent_at']
    success_message = "Nachricht erfolgreich aktualisiert!"
    success_url = "/user-dashboard/"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def test_func(self):
        notification = self.get_object()
        if self.request.user == notification.sender:
            return True
        else:
            return False

    def get_form(self):
        form = super().get_form()
        form.fields['incident_date'].widget = DateTimePickerInput(options={
            "format": "DD.MM.YYYY HH:mm",
            "locale": "de",
        })
        return form


class MessageDeleteView(generic.DeleteView):
    model = Message
    success_message = "Nachricht erfolgreich gelöscht!"
    success_url = "/user-dashboard/"

    def test_func(self):
        message = self.get_object()
        if self.request.user == message.sender:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MessageDeleteView, self).delete(request, *args, **kwargs)
