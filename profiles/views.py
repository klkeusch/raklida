import datetime
from django.utils import timezone

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from chartjs import *
from json import dumps

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from .models import *
from usernotifications.models import Message
from sensorvalues.models import *
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, DeviceChoiceField


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Benutzer erfolgreich registriert!")
            return redirect('blog_list')
    else:
        form = RegisterForm()
    return render(request, "profiles/register.html", {'form': form})


def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    assigned_profile = get_object_or_404(Profile, pk=pk)

    # if request.user.is_authenticated:
    # d = Profile.get_assigned_devices(self=pk)
    # assigned_devices = get_list_or_404(d)
    # else:
    #     assigned_devices = "Kein Gerät"

    context = {
        'user': user,
        'assigned_profile': assigned_profile,
        # 'assigned_devices': assigned_devices,
    }
    return render(request, "profiles/profile.html", context)


@login_required
def update(request):
    if request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form and profile_form:
            user_form.save()
            profile_form.save()
            messages.success(request, "Profil erfolgreich aktualisiert!")
            return redirect('profile', request.user.pk)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profiles/update.html', context)


# @login_required
@user_passes_test(lambda u: u.groups.filter(name='Verwaltung').exists())
def staff_dashboard(request):
    return render(request, 'profiles/staff_dashboard.html')


# @login_required
@user_passes_test(lambda u: u.groups.filter(name='Benutzer').exists())
def user_dashboard(request):
    return render(request, 'profiles/user_dashboard.html')


# def get_latest_values_for_user(request, device):
#     latest_values_list = Datapoints.objects.order_by('-timestamp')[:1]
#     return render(request, "profiles/staff_dashboard.html", {'latest_values_list': latest_values_list})
#     # return render(request, "profiles/user_dashboard.html", {'latest_values': latest_values})
#
#
# def get_latest_values_for_user(self):
#     # latest_values = Datapoints.objects.latest('timestamp')[:1]
#     return self.objects.latest('timestamp')


# def get_users_devices(request, pk):
#     if request.user:
#         assigned_devices = get_list_or_404(profiles.models.Profile)
#     else:
#         assigned_devices = "Kein Gerät"
#     return render(request, "profiles/profile.html", {'assigned_devices': assigned_devices})


@user_passes_test(lambda u: u.groups.filter(name='Benutzer').exists())
def user_logged_in(request):
    # devices = DeviceUserAssignment.objects.count(request.user)#filter(request.user.id)
    # latest_values = Datapoints.objects.latest('timestamp')
    notifications = Message.objects.filter(sender=request.user)
    # user_devices = DeviceUserAssignment.objects.all()
    # notifications = Message.objects.all()
    context = {
        # 'devices': devices,
        # 'latest_values': latest_values,
        'notifications': notifications,
    }
    return render(request, "profiles/user_dashboard.html", context)


@user_passes_test(lambda u: u.groups.filter(name='Benutzer').exists())
def show_user_device(request):
    notifications = Message.objects.filter(sender=request.user)

    # device_list = DeviceChoiceField(request=request)
    device_list = DeviceChoiceField(user=request.user)

    query_current_values = None  # https://stackoverflow.com/questions/43974798/local-variable-might-be-referenced-before-assignment-python/43974931

    query_current_device_display_name = None
    query_current_ambient_temperature = None
    query_current_relative_humidity = None
    query_current_air_quality = None
    query_current_co2_concentration = None
    query_current_barometric_pressure = None
    query_current_finedust_concentration = None
    query_current_last_update = None

    query_current_ambient_temperature_graph_data = None

    current_device_display_name = None
    current_ambient_temperature = None
    current_relative_humidity = None

    labels = []
    data = []

    time_24_hours_ago = timezone.localtime() - timezone.timedelta(days=1)

    if request.GET.get('devices'):
        selected_device = request.GET.get('devices')

        query_results = Devices.objects.filter(
            display_name=selected_device)

        query_current_values = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device)

        query_current_device_display_name = Devices.objects.filter(
            display_name=selected_device
        ).values_list(
            'display_name',
            flat=True
        ).distinct()
        current_device_display_name = [item for item in query_current_device_display_name]

        query_current_ambient_temperature = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device).filter(
            mqtt_node__name="ambient_temperature"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_relative_humidity = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device).filter(
            mqtt_node__name="relative_humidity"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_co2_concentration = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device).filter(
            mqtt_node__name="co2_concentration"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_barometric_pressure = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device).filter(
            mqtt_node__name="barometric_pressure"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_finedust_concentration = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device).filter(
            mqtt_node__name="pm2.5_atm"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_integer',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_air_quality = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device).filter(
            mqtt_node__name="air_quality"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_integer',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_last_update = Devices.objects.filter(
            display_name=selected_device
        ).values_list(
            'datapoints__last_update',
            flat=True
        ).latest(
            'last_status_update'
        )

        query_current_ambient_temperature_graph_data = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="ambient_temperature"
        ).values_list(
            'datapoint__data__value_double',
            flat=True
        ).filter(
            datapoint__data__timestamp__gte=time_24_hours_ago
        ).distinct()

        queryset_double_values = Data.objects.filter(
            # datapoint__device__deviceuserassignment__assigned_user=request.user.id,
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_ambient_temperature',
            timestamp__gte=time_24_hours_ago
        ).values_list(
            'value_double',
            flat=True
        ).exclude(
            value_double='-1.0'
        ).order_by('timestamp').distinct(

        )

        queryset_timestamps = Data.objects.filter(
            #datapoint__device__deviceuserassignment__assigned_user=request.user.id,
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_ambient_temperature',
            timestamp__gte=time_24_hours_ago
        ).values_list(
            'timestamp',
            flat=True
        ).exclude(
            value_double='-1.0'
        ).order_by('timestamp').distinct(

        )
        data = list(queryset_double_values)
        labels = list(queryset_timestamps)

    else:
        query_results = Devices.objects.none()

    context = {
        'notifications': notifications,
        'query_results': query_results,
        'query_current_values': query_current_values,
        'device_list': device_list,
        'current_device_display_name': current_device_display_name,

        'query_current_device_display_name': query_current_device_display_name,
        'query_current_ambient_temperature': query_current_ambient_temperature,
        'query_current_relative_humidity': query_current_relative_humidity,
        'query_current_co2_concentration': query_current_co2_concentration,
        'query_current_barometric_pressure': query_current_barometric_pressure,
        'query_current_air_quality': query_current_air_quality,
        'query_current_finedust_concentration': query_current_finedust_concentration,
        'query_current_last_update': query_current_last_update,

        'query_current_ambient_temperature_graph_data': query_current_ambient_temperature_graph_data,

        'current_ambient_temperature': current_ambient_temperature,
        'current_relative_humidity': current_relative_humidity,

        # 'queryset_double_values':queryset_double_values,
        # 'queryset_timestamps': queryset_timestamps,
        'labels': labels, # dumps('')?
        'data': data,
    }

    return render(request, "profiles/user_dashboard.html", context)


def line_chart(request):
    time_24_hours_ago = timezone.localtime() - timezone.timedelta(days=1)

    queryset_double_values = Data.objects.filter(
        datapoint__device__deviceuserassignment__assigned_user=request.user.id,
        datapoint__name='bme680_ambient_temperature',
        timestamp__gte=time_24_hours_ago
    ).values_list(
        'value_double',
        flat=True
    ).exclude(
        value_double='-1.0'
    ).order_by('timestamp').distinct(

    )

    queryset_timestamps = Data.objects.filter(
        datapoint__device__deviceuserassignment__assigned_user=request.user.id,
        datapoint__name='bme680_ambient_temperature',
        timestamp__gte=time_24_hours_ago
    ).values_list(
        'timestamp',
        flat=True
    ).exclude(
        value_double='-1.0'
    ).order_by('timestamp').distinct(

    )

    data = list(queryset_double_values)
    labels = list(queryset_timestamps)

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    },)
