import csv
from io import StringIO

def json_from(contents):
    data = StringIO(contents.read().decode('utf-8'))
    reader = csv.DictReader(data, delimiter=',')
    for row in reader:
        yield row

def import_data(contents):
    """A function which reads converts the contents
    of a CSV file into an array of JSON serializable
    properties, validated and ready for
    conversion to Defect model objects"""
    return [item for item in json_from(contents)]

    return [
        {
            'date_created': '3/03/2017',
            'description': 'Some description',
            'comments': 'Example comments',
            'status': 'Open',
            'priority': 'High',
            'reference': 'A title'
        },
        {
            'date_created': '4/03/2017',
            'description': 'Some description',
            'comments': 'Example comments',
            'status': 'Open',
            'priority': 'High',
            'reference': 'A title'
        },
        {
            'date_created': '5/03/2017',
            'description': 'Some description',
            'comments': 'Example comments',
            'status': 'Open',
            'priority': 'High',
            'reference': 'A title'
        }
    ]