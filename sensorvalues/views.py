from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required
import django_tables2 as tables
from .tables import DataTable
from .models import Data, Devices, DevicesTable


class DataListView(generic.ListView):
    model = Data
    ordering = ['-timestamp']
    paginate_by = 10


class DevicesListView(generic.ListView):
    model = Devices


# def devices_list(request): not working
#     devices = Devices.objects.all()
#
#     return render(request, "sensorvalues/devices_list.html", {"devices": devices})
#
#
# def chartjstest(request): not working
#     devices = Devices.objects.all()
#     return render(request, "sensorvalues/chartjs-test.html", {"devices": devices})


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


from django.http import JsonResponse


def get_devices_ajax(request):
    if request.method == "POST":
        device_id = request.POST['device_id']
        try:
            device = Devices.objects.filter(id=id).first()
            device_name = Devices.objects.filter(display_name=device_id)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(device.values('id', 'title')), safe=False)
