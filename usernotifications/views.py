from django.views import generic
from django.contrib import messages
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

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def test_func(self):
        notification = self.get_object()
        if self.request.user == notification.sender:
            return True
        else:
            return False


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
