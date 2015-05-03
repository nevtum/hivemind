from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(http_method_names=['POST'])
def accept(request):
    if 'COMMAND' in request.META.keys():
        command_type = request.META['COMMAND']
        # to call command handler
        return Response(request.data)

    data = {
        'message': 'Please provide a COMMAND type in request header',
        'request-data': request.data
    }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)
