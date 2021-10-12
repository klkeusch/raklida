from django.urls import path
from . import views

urlpatterns = [
    # path('statistics/', views.statistics_view, name='shop-statistics'),  # new
    # path('get-devices-ajax/', get_devices_ajax, name="get_devices_ajax"),
    path('devices/', views.DevicesListView.as_view(), 'devices_list'),
    # path('devices_list/', views.devices_list, 'devices_listing'),not working
    # path('chartjs-test/', views.chartjstest, 'chartjs-test'),not working
]
