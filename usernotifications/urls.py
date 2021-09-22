from django.urls import path
from . import views

urlpatterns = [
    # path("", views.MessageListView.as_view(), name="messages_list"),
    path("messages/", views.MessageListView.as_view(), name="messages_list"),
    path("messages/<int:pk>", views.MessageDetailView.as_view(), name="message_detail"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/update", views.MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete", views.MessageDeleteView.as_view(), name="message_delete"),
]
