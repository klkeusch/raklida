from django.shortcuts import render
import django_tables2 as tables
from .tables import DataTable
from .models import Data, Devices, DevicesTable


def data_list(request):
    table = DataTable(Data.objects.all())

    return render(request, "sensorvalues/sensorvalues_list.html", {"table": table})


class DevicesTableView(tables.SingleTableView):
    table_class = DevicesTable
    queryset = Devices.objects.all()
    template_name = "devices_list.html"
