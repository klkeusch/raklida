from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
import django_tables2 as tables
from .tables import DataTable
from .models import Data, Devices, DevicesTable


class DataListView(generic.ListView):
    model = Data
    ordering = ['-timestamp']
    paginate_by = 10


# class DataTableView(tables.SingleTableView):
# table_class = DataTable
# queryset = Data.objects.all()
# template_name = "sensorvalues_list.html"

def data_list(request):
    table = DataTable(Data.objects.all())

    return render(request, "sensorvalues/sensorvalues_list.html", {"table": table})


class DevicesTableView(tables.SingleTableView):
    table_class = DevicesTable
    queryset = Devices.objects.all()
    template_name = "devices_list.html"
