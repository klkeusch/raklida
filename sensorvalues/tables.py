import django_tables2 as tables
from .models import Data


# from .views import data_list


class DataTable(tables.Table):
    # display_name = tables.Column(accessor='datapoint.display_name')

    class Meta:
        model = Data
        sequence = ('timestamp', 'id', 'datapoint', 'value_string', 'value_integer', 'value_double', 'is_valid')
        exclude = ()
