from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render
import django_tables2 as tables
from .tables import DataTable
from .models import *
from profiles.models import Profile
from django.contrib.auth.models import User
from .util import download_csv

staff_csv_export_timeframe = timezone.localtime() - timezone.timedelta(days=14)


def export_devices_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    data = download_csv(request, Devices.objects.all())
    response = HttpResponse(data, content_type='text/csv')
    return response


def export_data_csv(request):
    data = download_csv(
        request,
        Data.objects.all().filter(
            timestamp__gte=staff_csv_export_timeframe
        )
    )
    response = HttpResponse(data, content_type='text/csv')
    return response


def export_datapoints_csv(request):
    data = download_csv(request, Datapoints.objects.all())
    response = HttpResponse(data, content_type='text/csv')
    return response


def export_mqtt_tree_nodes_csv(request):
    data = download_csv(request, MqttTreeNodes.objects.all())
    response = HttpResponse(data, content_type='text/csv')
    return response


def export_mqtt_tree_datapoint_translations_csv(request):
    data = download_csv(request, TreeDatapointTranslations.objects.all())
    response = HttpResponse(data, content_type='text/csv')
    return response


# def data_list(request):
#     table = DataTable(Data.objects.all())
#
#     return render(request, "sensorvalues/sensorvalues_list.html", {"table": table})
#
#
# class DevicesTableView(tables.SingleTableView):
#     table_class = DevicesTable
#     queryset = Devices.objects.all()
#     template_name = "devices_list.html"
