from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from sensorvalues.models import Datapoints


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
    return render(request, "profiles/profile.html", {'user': user})


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


def get_latest_values_for_user(request, device):
    latest_values_list = Datapoints.objects.order_by('-timestamp')[:1]
    return render(request, "profiles/staff_dashboard.html", {'latest_values_list': latest_values_list})
    # return render(request, "profiles/user_dashboard.html", {'latest_values': latest_values})
