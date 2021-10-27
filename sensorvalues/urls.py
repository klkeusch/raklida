from django.urls import path

import sensorvalues.models
from . import views

urlpatterns = [
    # path('devices/', views.DevicesListView.as_view(), 'devices_list'),
    # Exports below
    path('export-csv/devices', views.export_devices_csv, name='export_devices_csv'),
    path('export-csv/data', views.export_data_csv, name='export_data_csv'),
    path('export-csv/datapoints', views.export_datapoints_csv, name='export_datapoints_csv'),
    path('export-csv/mqtt-tree-nodes', views.export_mqtt_tree_nodes_csv, name='export_mqtt_tree_nodes_csv'),
    path('export-csv/mqtt-tree-datapoint-translations', views.export_mqtt_tree_datapoint_translations_csv,
         name='export_mqtt_tree_datapoint_translations_csv'),
    # Exports above
]
