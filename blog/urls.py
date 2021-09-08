from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_blogs, name="blog_list"),
    path("blog/<int:pk>", views.detail_blog, name="blog_detail"),
]
