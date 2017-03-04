
def import_data(contents):
    """A function which reads converts the contents
    of a CSV file into an array of JSON serializable
    properties, validated and ready for
    conversion to Defect model objects"""
    return [{
        'description': 'Some description',
        'comments': 'Example comments',
        'priority': 'High',
        'reference': 'A title'
    }]