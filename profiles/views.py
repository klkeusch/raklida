from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
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


# def show_user_device(request):
#     device_list = DeviceChoiceField()
#
#     # selected_device = request.GET.get('devices')
#     # query_results = DeviceUserAssignment.objects.filter(device=selected_device).filter(
#     #     assigned_user=request.pro)  # .filter(field von model = selected_device)
#
#     if request.GET.get('devices'):
#         selected_device = request.GET.get('devices')
#         # print(selected_device)
#         # query_results = Devices.objects.filter(profile__assigned_devices__display_name=selected_device)#(display_name=selected_device)
#         query_results = DeviceUserAssignment.objects.filter(device__display_name=selected_device)#.filter(assigned_user_id=request.user.pk)  # .filter(field von model = selected_device)
#     else:
#         query_results = Devices.objects.none()
#
#     context = {
#         'device_list': device_list,
#         'query_results': query_results,
#         'selected_device': selected_device,
#     }
#
#     return render(request, "profiles/user_dashboard.html", context)


def show_user_device(request):
    device_list = DeviceChoiceField(request=request)

    if request.GET.get('devices'):
        selected_device = request.GET.get('devices')
        # query_results = Devices.objects.filter(profile__assigned_devices__display_name=selected_device)#(display_name=selected_device)
        query_results = Devices.objects.filter(
            display_name=selected_device)  # .filter(assigned_user_id=request.user.pk)  # .filter(field von model = selected_device)
       #  query_current_values = TreeDatapointTranslations.objects.filter(datapoint__device__display_name=selected_device).latest("datapoint__name")
    else:
        query_results = Devices.objects.none()

    context = {
        'query_results': query_results,
        'device_list': device_list,
       # 'query_current_values': query_current_values,
    }

    return render(request, "profiles/user_dashboard.html", context)
