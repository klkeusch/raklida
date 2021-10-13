import django_tables2 as tables
from .models import Data


class DataTable(tables.Table):

    class Meta:
        model = Data
        sequence = ('timestamp', 'id', 'datapoint', 'value_string', 'value_integer', 'value_double', 'is_valid')
        exclude = ()
