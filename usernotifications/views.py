from django.views import generic
from django.contrib import messages
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Message
from .forms import MessageCreateForm, MessageUpdateForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class MessageListView(LoginRequiredMixin, generic.ListView):
    model = Message

    def get_queryset(self, *args, **kwargs):
        return Message.objects.filter(sender=self.request.user)


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Message
    form_class = MessageCreateForm
    success_url = "/messages/"
    success_message = "Nachricht erfolgreich erstellt!"

    # def get_form(self):
    #     form = super().get_form()
    #     form.fields['incident_date'].widget = DateTimePickerInput(options={
    #         "format": "DD.MM.YYYY HH:mm",
    #         "locale": "de",
    #     }, )
    # form.fields['recipient'].queryset = User.objects.values_list('username', flat=True).exclude(
    #     is_staff=False).exclude(username=self.request.user)

    # form.fields['user_devices'].queryset = DeviceUserAssignment.objects.filter(
    #     device__profile__user=self.request.user
    # ).values_list(
    #     "device__profile__assigned_devices__display_name",
    #     flat=True
    # ).distinct()
    # return form

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='Benutzer').exists()


class MessageDetailView(generic.DetailView):
    model = Message


class MessageUpdateView(generic.UpdateView):
    model = Message
    form_class = MessageUpdateForm
    success_message = "Nachricht erfolgreich aktualisiert!"
    success_url = "/messages/"

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
    success_url = "/messages/"

    def test_func(self):
        message = self.get_object()
        if self.request.user == message.sender:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MessageDeleteView, self).delete(request, *args, **kwargs)
