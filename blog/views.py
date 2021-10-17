"""Views for blog app"""
from .models import Blog
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


class BlogListView(generic.ListView):
    """Class-based view for listing blog entries.

    :returns: page with lists of blog entries.
    """
    model = Blog
    ordering = ['-date_published']
    paginate_by = 3


class BlogDetailView(generic.DetailView):
    """Class-based view for viewing blog entries.

    :returns: detail page of blog entry.
    """
    model = Blog


class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """Class-based view for creating blog entries.

    :returns: create page for blog entry .
    """
    model = Blog
    fields = ['title', 'content']
    success_message = "Blogeintrag erfolgreich erstellt!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, generic.UpdateView):
    """Class-based view for updating blog entries.

    :returns: update page for blog entry .
    """
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
    """Class-based view for deleting blog entries.

    :returns: delete page for blog entry .
    """
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
