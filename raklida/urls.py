"""raklida URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from profiles import views as profiles_views
from sensorvalues import views as sensorvalues_views
from sensorvalues import tables as tables

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('blog.urls')),
    # Sensorvalues below
    path("sensorvalues/", sensorvalues_views.data_list, name="sensorvalues_list"),
    path("sensorvalues/devices", sensorvalues_views.DevicesTableView.as_view(template_name="sensorvalues/devices_list.html.html"),
         name="devices_list"),
    #path("sensorvalues/", sensorvalues_views.DataListView.as_view(template_name="sensorvalues/sensorvalues_list.html"),
    #     name="sensorvalues_list"),
    # Sensorvalues above
    # User related paths below
    path("register/", profiles_views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="profiles/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="profiles/logout.html"), name="logout"),
    path("profile/<int:pk>", profiles_views.profile, name="profile"),
    path("profile/update", profiles_views.update, name="update"),
    # User related paths above
    # password reset below
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="profiles/password_reset.html"),
         name="password_reset"),
    path('password-reset/confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="profiles/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name="profiles/password_reset_done.html"),
         name="password_reset_done"),
    path('password-reset/complete',
         auth_views.PasswordResetCompleteView.as_view(template_name="profiles/password_reset_complete.html"),
         name="password_reset_complete"),
    # password reset above
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
