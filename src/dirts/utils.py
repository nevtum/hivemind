import csv
import re
from io import StringIO

from django.utils.timezone import datetime

from .forms import ImportDirtForm
from .models import Status, Priority
from django.shortcuts import get_object_or_404
from .serializers import ImportDefectSerializer

def parse_datetime(datestring) -> datetime:
    expr = re.compile('^(?P<day>\d{1,2})\/(?P<month>\d{1,2})\/(?P<year>\d{4})$')
    match = expr.match(datestring)
    if not match:
        raise ValueError('Incorrect date format. Should be dd/mm/yyyy.')
    kw = match.groupdict()
    day = int(kw['day'])
    month = int(kw['month'])
    year = int(kw['year'])
    return datetime(year, month, day)

def _format_priority(priority):
    if priority.lower() == 'high':
        return 'High'
    if priority.lower() == 'medium':
        return 'Medium'
    if priority.lower() == 'low':
        return 'Low'
    if priority.lower() == 'observation':
        return 'Observational'
    raise ValueError("Unknown priority string: %s" % priority)

def _format_status(status):
    if status.lower() == 'open':
        return 'Open'
    if status.lower() == 'closed':
        return 'Closed'
    raise ValueError("Unknown status string: %s" % status)

def json_from(request) -> list:
    contents = request.FILES['import_file']
    code = request.POST['project_code']
    data = StringIO(contents.read().decode('utf-8'))
    reader = csv.DictReader(data, delimiter=',')
    for row in reader:
        status = get_object_or_404(Status, name=_format_status(row['Status']))
        priority = get_object_or_404(Priority, name=_format_priority(row['Priority']))
        date_created = parse_datetime(row['Date Created'])
        data = {
            'date_created': date_created,
            'description': row['Description'],
            'comments': row['Comments'],
            'submitter': request.user.username,
            'status': status.name,
            'priority': priority.name,
            'reference': row['Reference'],
            'release_id': row['Version'],
            'date_closed': row['Date Closed'],
            'project_code': code
        }
        serializer = ImportDefectSerializer(data=data)
        if not serializer.is_valid():
            yield {
                'errors': serializer.errors
            }
        yield serializer.data


def import_data(request):
    """A function which reads converts the contents
    of a CSV file into an array of JSON serializable
    properties, validated and ready for
    conversion to Defect model objects"""
    return [item for item in json_from(request)]
