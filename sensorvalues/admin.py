from django.contrib import admin
# Info: Django Dropdown Filter tauchen erst ab >4 Einträgen auf
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib.admin import SimpleListFilter
from .models import Data, Datapoints, Devices, MqttTreeNodes, TreeDatapointTranslations, DevicesTable, DailyAverages, \
    DeviceUserAssignment
from related_admin import RelatedFieldAdmin, getter_for_related_field
from admincharts.admin import AdminChartMixin
from admincharts.utils import months_between_dates
from django.utils import timezone
from json import dumps, dump

# admin.site.register(Datapoints)
# admin.site.register(MqttTreeNodes)
# admin.site.register(TreeDatapointTranslations)
admin.site.register(DailyAverages)


class TreeDatapointTranslationsAdmin(admin.ModelAdmin):
    model = TreeDatapointTranslations
    sortable_by = ('datapoint', 'mqtt_node', 'id')
    list_filter = ('datapoint__device', 'mqtt_node__name',)
    list_display = ('id', 'datapoint', 'mqtt_node',)
    # list_editable = ('datapoint', 'mqtt_node')
    # list_display_links = list_display


class MqttTreeNodesAdmin(admin.ModelAdmin):
    model = MqttTreeNodes
    sortable_by = ('parent_id', 'is_leaf', 'name', 'id')
    list_filter = ('name', 'is_leaf', 'parent_id',)
    list_display = ('id', 'name', 'parent_id', 'is_leaf',)
    list_display_links = ('id', 'name',)


class DevicesAdmin(admin.ModelAdmin):
    model = Devices
    # list_display = ('id', 'display_name', 'location', 'last_status_update', 'in_rooms')
    list_display = ('id', 'display_name', 'location', 'last_status_update',)
    list_display_links = ('id', 'display_name')
    list_filter = (
        ('location', DropdownFilter),
        # ('deviceuserassignment__assigned_user__', DropdownFilter),

    )
    search_fields = ('assigned_user', 'device',)


# class DevicesAdmin(RelatedFieldAdmin):
#     # model = Devices
#     list_display = ('id', 'display_name', 'location', 'last_status_update', 'in_rooms', 'assigned_to_user')


class DevicesUserAssignmentAdmin(admin.ModelAdmin):
    model = DeviceUserAssignment
    fields = ['assigned_user', 'device', 'usage_reason', ('start_date', 'end_date')]
    list_display = ('id', 'assigned_user', 'device', 'usage_reason', 'start_date', 'end_date',)
    list_display_links = list_display
    list_filter = (
        ('assigned_user', RelatedDropdownFilter),
        ('device', RelatedDropdownFilter)
    )
    # search_fields = ('assigned_user', 'device',)
    # autocomplete_fields = ['assigned_user', 'device',]


class DataAdmin(AdminChartMixin, admin.ModelAdmin):
    model = Data
    list_display_links = ['id', 'timestamp', 'datapoint']
    list_display = ('id', 'timestamp', 'datapoint', 'value_double', 'value_integer', 'value_string', 'is_valid')
    list_filter = (
        'timestamp',
        ('datapoint__device__display_name', DropdownFilter),
        ('datapoint__device__deviceuserassignment__assigned_user', RelatedDropdownFilter),
        ('datapoint__name', DropdownFilter),
    )

    list_chart_type = "line"
    #list_chart_data = {}
    list_chart_options = {
        "aspectRatio": 3,
        "scales[x].type": "time",
        "options.scales[x].ticks.autoskip": True,
    }
    #list_chart_config = None  # Override the combined settings

    def get_list_chart_queryset(self, result_list):
        result_list = Data.objects.all()#values_list('value_double', flat=True)
        return result_list

    # def get_list_chart_type(self, queryset):
    #     pass

    def get_list_chart_data(self, queryset):
        if not queryset:
            return {}

        # Cannot reorder the queryset at this point
        earliest = min([x.timestamp for x in queryset])

        labels = []
        totals = []
        for b in months_between_dates(earliest, timezone.now()):
            labels.append(b.strftime("%b %Y"))

        qs = Data.objects.values_list(
            'value_double',
            flat=True
        ).order_by(
            'timestamp'
        ).distinct()

        qs2 = Data.objects.filter(
            datapoint__name='bme680_ambient_temperature',
        ).values_list(
            'timestamp',
            flat=True
        ).order_by(
            'timestamp'
        ).distinct()

        totals = list(qs)
        labels = list(qs2)
        # totals.append(
        #     len(
        #         [
        #             x
        #             for x in queryset
        #             if x.timestamp.year == b.year and x.timestamp.month == b.month
        #         ]
        #     )
        # )

        return {
            "labels": labels,
            "datasets": [
                {"label": "Datapoint values_double", "data": totals, "backgroundColor": "#79aec8"},
            ],
        }

    # def get_list_chart_options(self, queryset):
    #     pass
    #
    # def get_list_chart_config(self, queryset):
    #     pass


class DatapointAdmin(AdminChartMixin, admin.ModelAdmin):
    model = Datapoints
    list_filter = (
        ('device', RelatedDropdownFilter),
        ('device__deviceuserassignment__assigned_user', RelatedDropdownFilter),
        ('name', DropdownFilter)
    )
    list_display = (
        'id', 'name', 'display_name', 'unit', 'device', 'current_value_double', 'current_value_integer',
        'current_value_string',
        'last_update', 'store_historic_data')
    # list_editable = ('display_name', 'unit', 'device', 'current_value_double', 'current_value_integer', 'current_value_string',
    #     'last_update', 'store_historic_data')
    list_display_links = list_display

    list_chart_type = "line"
    list_chart_data = {}
    list_chart_options = {"aspectRatio": 6}
    list_chart_config = None  # Override the combined settings

    def get_list_chart_data(self, queryset):
        if not queryset:
            return {}

        # Cannot reorder the queryset at this point
        earliest = min([x.last_update for x in queryset])

        labels = []
        totals = []
        for b in months_between_dates(earliest, timezone.now()):
            labels.append(b.strftime("%b %Y"))
            totals.append(
                len(
                    [
                        x
                        for x in queryset
                        if x.last_update.year == b.year and x.last_update.month == b.month
                    ]
                )
            )

        return {
            "labels": labels,
            "datasets": [
                {"label": "Datapoint values_double", "data": totals, "backgroundColor": "#79aec8"},
            ],
        }


admin.site.register(Devices, DevicesAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(DeviceUserAssignment, DevicesUserAssignmentAdmin)
admin.site.register(Datapoints, DatapointAdmin)
admin.site.register(MqttTreeNodes, MqttTreeNodesAdmin)
admin.site.register(TreeDatapointTranslations, TreeDatapointTranslationsAdmin)
