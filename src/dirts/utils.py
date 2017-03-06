import csv
import re
from io import StringIO

from django.utils.timezone import datetime

from .forms import CreateDirtForm

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

def json_from(request) -> list:
    contents = request.FILES['import_file']
    code = request.POST['project_code']
    submitter = request.user.username
    data = StringIO(contents.read().decode('utf-8'))
    reader = csv.DictReader(data, delimiter=',')
    for row in reader:
        date_created = parse_datetime(row['Date Created'])
        yield {
            'date_created': date_created,
            'description': row['Description'],
            'comments': row['Comments'],
            'priority': row['Priority'],
            'status': row['Status'],
            'reference': row['Reference'],
            'version': row['Version'],
            'date_closed': row['Date Closed'],
            'owner': submitter,
            'project_code': code
        }

def validated(input: list) -> list:
    for data in input:
        # form = CreateDirtForm(**data)
        yield data


def import_data(request):
    """A function which reads converts the contents
    of a CSV file into an array of JSON serializable
    properties, validated and ready for
    conversion to Defect model objects"""
    mapping = json_from(request)
    mapping = validated(mapping)
    return [item for item in mapping]
