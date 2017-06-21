from rest_framework.exceptions import ParseError
from rest_framework.decorators import api_view
from rest_framework.response import Response

_handlers = {}

@api_view(http_method_names=['POST'])
def accept(request):
    """Processes a command where COMMAND must be set in the
    request header and a JSON payload in the body. Command handler
    must accept HTTP POST methods only.
    
    'Authorization: JWT [your_token]' must also be included in 
    the header for permission to POST."""
    command_type = request.META.get('HTTP_COMMAND')

    if command_type is None:
        error = 'Please provide a COMMAND type in request header'
        raise ParseError(detail=error)

    if not command_type in _handlers:
        error = 'Could not find a handler for the given COMMAND type'
        raise ParseError(detail=error)
    
    command_handler = _handlers[command_type]
    response_data = command_handler.process(request.GET)
    return Response(request.data)