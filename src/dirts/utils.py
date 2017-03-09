import csv
import re
from io import StringIO

from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime
from rest_framework.serializers import ValidationError

from .models import Priority, Status
from .serializers import ImportDefectSerializer

def _format_priority(priority):
    if priority.lower() == 'high':
        return 'High'
    if priority.lower() == 'medium':
        return 'Medium'
    if priority.lower() == 'low':
        return 'Low'
    if priority.lower() == 'observation':
        return 'Observational'
    raise ValidationError("Unknown priority string: %s" % priority)

def _format_status(status):
    if status.lower() == 'open':
        return 'Open'
    if status.lower() == 'closed':
        return 'Closed'
    raise ValidationError("Unknown status string: %s" % status)

def json_from(request) -> list:
    contents = request.FILES['import_file']
    code = request.POST['project_code']
    data = StringIO(contents.read().decode('utf-8'))
    reader = csv.DictReader(data, delimiter=',')
    for row in reader:
        if row['Date Closed'] != '':
            date_closed = row['Date Closed']
        else:
            date_closed = None
        data = {
            'date_created': row['Date Created'],
            'description': row['Description'],
            'comments': row['Comments'],
            'submitter': request.user.username,
            'status': _format_status(row['Status']),
            'priority': _format_priority(row['Priority']),
            'reference': row['Reference'],
            'release_id': row['Version'],
            'date_changed': date_closed,
            'project_code': code
        }
        serializer = ImportDefectSerializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        yield serializer.data


def import_data(request):
    """A function which reads converts the contents
    of a CSV file into an array of JSON serializable
    properties, validated and ready for
    conversion to Defect model objects"""
    return [item for item in json_from(request)]
