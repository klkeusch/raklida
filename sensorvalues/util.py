import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse


# European format: . -> , 15102021
def localize_floats(row):
    """ Function for switching . to , for csv export.

    :param row: current value row

    :returns: Corrected row.
    """
    return [
        str(el).replace('.', ',') if isinstance(el, float) else el
        for el in row
    ]


def download_csv(request, queryset):
    """ Function collects and exports data to csv.

    :param request: .
    :param queryset: queryset for model

    :returns: Http response with csv values.
    """
    if not request.user.is_staff:
        raise PermissionDenied

    model = queryset.model
    model_fields = model._meta.fields + model._meta.many_to_many
    field_names = [field.name for field in model_fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'

    # the csv writer
    writer = csv.writer(response, delimiter=";")
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows

    for row in queryset:
        values = []
        for field in field_names:
            value = getattr(row, field)
            if callable(value):
                try:
                    value = value() or ''
                except ValueError:  # ValueError added 14102021
                    value = 'Error retrieving value'
            if value is None:
                value = ''
            values.append(value)
        writer.writerow(localize_floats(values))
    return response
