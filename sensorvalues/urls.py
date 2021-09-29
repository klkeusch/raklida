from django.urls import path
from . import views

urlpatterns = [
    # path('get-devices-ajax/', get_devices_ajax, name="get_devices_ajax"),
    path('devices/', views.DevicesListView.as_view(), 'devices_list'),
    path('devices_list/', views.devices_list, 'devices_listing')
]
