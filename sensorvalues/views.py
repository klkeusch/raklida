from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
import django_tables2 as tables
from .models import Data, SimpleTable


class DataListView(generic.ListView):
    model = Data
    ordering = ['-timestamp']
    paginate_by = 10


class TableView(tables.SingleTableView):
    table_class = SimpleTable
    queryset = Data.objects.all()
    template_name = "sensorvalues_list.html"
