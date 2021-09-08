from django.shortcuts import render, get_object_or_404
from .models import Blog
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


class BlogListView(generic.ListView):
    model = Blog
    ordering = ['-date_published']
    paginate_by = 3


class BlogDetailView(generic.DetailView):
    model = Blog


class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Blog
    fields = ['title', 'content']
    success_message = "Blogeintrag erfolgreich erstellt!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, generic.UpdateView):
    model = Blog
    fields = ['title', 'content']
    success_message = "Blogeintrag erfolgreich aktualisiert!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        else:
            return False


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Blog
    success_message = "Blog erfolgreich gelöscht!"
    success_url = "/"

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BlogDeleteView, self).delete(request, *args, **kwargs)
