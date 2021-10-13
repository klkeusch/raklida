from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.DevicesListView.as_view(), 'devices_list'),
]
