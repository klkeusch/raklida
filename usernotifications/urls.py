from django.urls import path
from . import views

urlpatterns = [
    path("messages/", views.MessageListView.as_view(), name="messages_list"),
]
