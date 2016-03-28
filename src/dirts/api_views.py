from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, api_view, permission_classes
from rest_framework.permissions import AllowAny
from common import store as EventStore
from common.serializers import DomainEventSerializer
from .models import Defect
from .serializers import DefectSerializer

class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        events = EventStore.get_events_for('DEFECT', id)
        serializer = DomainEventSerializer(events, many=True)
        return Response(serializer.data)
        
    @detail_route(methods=['put'])
    def close(self):
        """Custom method and route for closing existing DIRT"""
        pass
    
    @detail_route(methods=['put'])
    def reopen(self):
        """Custom method and route for reopening existing DIRT"""
        pass

@api_view(['GET'])
@permission_classes((AllowAny, ))
def autocomplete(request):
    keyword = request.GET.get('q', '')
    results = []
    if len(keyword) > 2:
        result_set = Defect.objects.filter(reference__icontains=keyword)
        for obj in result_set.distinct()[:10]:
            results.append({
                'title': obj.reference
            })
    return Response(results)