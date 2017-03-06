import csv
from io import StringIO

def json_from(request):
    contents = request.FILES['import_file']
    code = request.POST['project_code']
    submitter = request.user.username
    # import pdb; pdb.set_trace()
    data = StringIO(contents.read().decode('utf-8'))
    reader = csv.DictReader(data, delimiter=',')
    for row in reader:
        yield {
            'date_created': row['Date Created'],
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

def import_data(request):
    """A function which reads converts the contents
    of a CSV file into an array of JSON serializable
    properties, validated and ready for
    conversion to Defect model objects"""
    return [item for item in json_from(request)]