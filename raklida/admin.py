from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path


@staff_member_required
def admin_device_sensorvalues_view(request):
    return render(request, 'admin/device_sensorvalues.html', {'title': 'Messwerteverlauf - Geräte'})


class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list += [
            {
                'name': 'Diagramme',
                'app_label': 'sensorvalues_diagrams',
                'models': [
                    {
                        'name': 'Messwerteverlauf - Geräte',
                        'object_name': 'device-sensorvalues',
                        'admin_url': 'device-sensorvalues',
                        'view_only': True,
                    }
                ],
            }
        ]
        return app_list

    # def get_urls(self):
    #     urls = super().get_urls()
    #     urls += [
    #         path('device-sensorvalues/', admin_device_sensorvalues_view, name='admin-device-sensorvalues'),
    #     ]
    #     return urls
