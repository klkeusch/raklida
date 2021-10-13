from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
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

    context = {
        'user': user,
        'assigned_profile': assigned_profile,
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


@user_passes_test(lambda u: u.groups.filter(name='Verwaltung').exists())
def staff_dashboard(request):
    return render(request, 'profiles/staff_dashboard.html')


@user_passes_test(lambda u: u.groups.filter(name='Benutzer').exists())
def user_dashboard(request):
    return render(request, 'profiles/user_dashboard.html')


@user_passes_test(lambda u: u.groups.filter(name='Benutzer').exists())
def user_logged_in(request):
    notifications = Message.objects.filter(sender=request.user)

    context = {
        'notifications': notifications,
    }
    return render(request, "profiles/user_dashboard.html", context)


@user_passes_test(lambda u: u.groups.filter(name='Verwaltung').exists())
def staff_logged_in(request):
    notifications = Message.objects.all()

    context = {
        'notifications': notifications,
    }
    return render(request, "profiles/staff_dashboard.html", context)


@user_passes_test(lambda u: u.groups.filter(name='Benutzer').exists())
def show_user_device(request):
    notifications = Message.objects.filter(sender=request.user)

    device_list = DeviceChoiceField(user=request.user)

    query_current_values = None
    query_current_device_display_name = None
    query_current_ambient_temperature = None
    query_current_relative_humidity = None
    query_current_air_quality = None
    query_current_co2_concentration = None
    query_current_barometric_pressure = None
    query_current_finedust_concentration = None
    query_current_last_update = None
    current_device_display_name = None
    current_ambient_temperature = None
    current_relative_humidity = None

    """ Below Values for charting """
    labels = []
    ambient_temperature_chart_data = []
    relative_humidity_chart_data = []
    co2_concentration_chart_data = []
    pm2_5_atm_chart_data = []
    air_quality_chart_data = []
    barometric_pressure_chart_data = []
    """ Above Values for charting """

    user_graph_timeframe = timezone.localtime() - timezone.timedelta(days=1)

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
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="ambient_temperature"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_relative_humidity = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="relative_humidity"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_co2_concentration = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="co2_concentration"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_barometric_pressure = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="barometric_pressure"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_finedust_concentration = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="pm2_5_atm"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_integer',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_air_quality = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="air_quality"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_integer',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_last_update = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__last_update',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        """ Below gathering data for charts"""

        queryset_ambient_temperature_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_ambient_temperature',
            timestamp__gte=user_graph_timeframe
        ).values_list(
            'value_double',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_relative_humidity_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_relative_humidity',
            timestamp__gte=user_graph_timeframe
        ).values_list(
            'value_double',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_co2_concentration_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='scd30_co2_concentration',
            timestamp__gte=user_graph_timeframe
        ).values_list(
            'value_double',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_barometric_pressure_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_barometric_pressure',
            timestamp__gte=user_graph_timeframe
        ).values_list(
            'value_double',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_pm2_5_atm_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='pms5003_pm2_5_atm',
            timestamp__gte=user_graph_timeframe
        ).values_list(
            'value_integer',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_air_quality_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='mq135_air_quality',
            timestamp__gte=user_graph_timeframe
        ).values_list(
            'value_integer',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_timestamps = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_ambient_temperature',
            timestamp__gte=user_graph_timeframe
        ).values_list(
            'timestamp',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        relative_humidity_chart_data = list(queryset_relative_humidity_double_values)
        ambient_temperature_chart_data = list(queryset_ambient_temperature_double_values)
        co2_concentration_chart_data = list(queryset_co2_concentration_double_values)
        pm2_5_atm_chart_data = list(queryset_pm2_5_atm_double_values)
        air_quality_chart_data = list(queryset_air_quality_double_values)
        barometric_pressure_chart_data = list(queryset_barometric_pressure_double_values)
        labels = list(queryset_timestamps)

        """ Above gathering data for charts"""

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
        'current_ambient_temperature': current_ambient_temperature,
        'current_relative_humidity': current_relative_humidity,
        'labels': labels,
        'ambient_temperature_chart_data': ambient_temperature_chart_data,
        'relative_humidity_chart_data': relative_humidity_chart_data,
        'co2_concentration_chart_data': co2_concentration_chart_data,
        'barometric_pressure_chart_data': barometric_pressure_chart_data,
        'pm2_5_atm_chart_data': pm2_5_atm_chart_data,
        'air_quality_chart_data': air_quality_chart_data,
    }
    return render(request, "profiles/user_dashboard.html", context)


@user_passes_test(lambda u: u.groups.filter(name='Verwaltung').exists())
def show_staff_devices(request):
    notifications = Message.objects.all()

    devices_list = DeviceChoiceField(user=request.user)

    query_current_values = None

    query_current_device_display_name = None
    query_current_ambient_temperature = None
    query_current_relative_humidity = None
    query_current_air_quality = None
    query_current_co2_concentration = None
    query_current_barometric_pressure = None
    query_current_finedust_concentration = None
    query_current_last_update = None
    current_device_display_name = None
    current_ambient_temperature = None
    current_relative_humidity = None

    """ Below Values for charting """
    labels = []
    ambient_temperature_chart_data = []
    relative_humidity_chart_data = []
    co2_concentration_chart_data = []
    pm2_5_atm_chart_data = []
    air_quality_chart_data = []
    barometric_pressure_chart_data = []
    """ Above Values for charting """

    staff_graph_timeframe = timezone.localtime() - timezone.timedelta(days=14)

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
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="ambient_temperature"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_relative_humidity = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="relative_humidity"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_co2_concentration = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="co2_concentration"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_barometric_pressure = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="barometric_pressure"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_double',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_finedust_concentration = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="pm2_5_atm"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_integer',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_air_quality = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
            mqtt_node__name="air_quality"
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__current_value_integer',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        query_current_last_update = TreeDatapointTranslations.objects.filter(
            datapoint__device__display_name=selected_device
        ).filter(
        ).values_list(
            'mqtt_node__treedatapointtranslations__datapoint__last_update',
            flat=True
        ).latest(
            'mqtt_node__treedatapointtranslations__datapoint__last_update'
        )

        """ Below gathering data for charts"""

        queryset_ambient_temperature_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_ambient_temperature',
            timestamp__gte=staff_graph_timeframe
        ).values_list(
            'value_double',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_relative_humidity_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_relative_humidity',
            timestamp__gte=staff_graph_timeframe
        ).values_list(
            'value_double',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_co2_concentration_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='scd30_co2_concentration',
            timestamp__gte=staff_graph_timeframe
        ).values_list(
            'value_double',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_barometric_pressure_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_barometric_pressure',
            timestamp__gte=staff_graph_timeframe
        ).values_list(
            'value_double',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_pm2_5_atm_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='pms5003_pm2_5_atm',
            timestamp__gte=staff_graph_timeframe
        ).values_list(
            'value_integer',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_air_quality_double_values = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='mq135_air_quality',
            timestamp__gte=staff_graph_timeframe
        ).values_list(
            'value_integer',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        queryset_timestamps = Data.objects.filter(
            datapoint__device__display_name=selected_device,
            datapoint__name='bme680_ambient_temperature',
            timestamp__gte=staff_graph_timeframe
        ).values_list(
            'timestamp',
            flat=True
        ).exclude(
            datapoint__current_value_string="Offline",
        ).order_by(
            'timestamp'
        ).distinct()

        relative_humidity_chart_data = list(queryset_relative_humidity_double_values)
        ambient_temperature_chart_data = list(queryset_ambient_temperature_double_values)
        co2_concentration_chart_data = list(queryset_co2_concentration_double_values)
        pm2_5_atm_chart_data = list(queryset_pm2_5_atm_double_values)
        air_quality_chart_data = list(queryset_air_quality_double_values)
        barometric_pressure_chart_data = list(queryset_barometric_pressure_double_values)
        labels = list(queryset_timestamps)

        """ Above gathering data for charts"""

    else:
        query_results = Devices.objects.none()

    context = {
        'notifications': notifications,
        'query_results': query_results,
        'query_current_values': query_current_values,
        'devices_list': devices_list,
        'current_device_display_name': current_device_display_name,
        'query_current_device_display_name': query_current_device_display_name,
        'query_current_ambient_temperature': query_current_ambient_temperature,
        'query_current_relative_humidity': query_current_relative_humidity,
        'query_current_co2_concentration': query_current_co2_concentration,
        'query_current_barometric_pressure': query_current_barometric_pressure,
        'query_current_air_quality': query_current_air_quality,
        'query_current_finedust_concentration': query_current_finedust_concentration,
        'query_current_last_update': query_current_last_update,
        'current_ambient_temperature': current_ambient_temperature,
        'current_relative_humidity': current_relative_humidity,
        'labels': labels,
        'ambient_temperature_chart_data': ambient_temperature_chart_data,
        'relative_humidity_chart_data': relative_humidity_chart_data,
        'co2_concentration_chart_data': co2_concentration_chart_data,
        'barometric_pressure_chart_data': barometric_pressure_chart_data,
        'pm2_5_atm_chart_data': pm2_5_atm_chart_data,
        'air_quality_chart_data': air_quality_chart_data,
    }
    return render(request, "profiles/staff_dashboard.html", context)
