from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, api_view, permission_classes
from rest_framework.permissions import AllowAny
from common import store as EventStore
from common.models import Project
from common.serializers import DomainEventSerializer
from .models import Defect
from .serializers import DefectSerializer

class DefectBaseViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    permission_classes = [AllowAny]
        
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
def more_like_this_defect(request):
    DEFAULT_COUNT = '5'
    id = request.GET.get('id', '')
    if id == '':
        return Response("could not find id")

    count = request.GET.get('count', DEFAULT_COUNT)
    count = int(count)

    defect = Defect.objects.get(pk=id)
    similar = defect.more_like_this(count)
    similar = map(lambda x: x.object, similar)
    similar = map(lambda x: to_serializable(x), similar)

    data = {
        "current": to_serializable(defect),
        "similar": similar,
    }
    return Response(data)

def to_serializable(defect):
    return {
        "id": defect.id,
        "reference": defect.reference,
        "created": defect.date_created,
        "created_by": defect.submitter.username,
        "status": defect.status.name,
    }

@api_view(['GET'])
@permission_classes((AllowAny, ))
def autocomplete_projects(request):
    keyword = request.GET.get('q', '')
    results = []
    if len(keyword) > 2:
        query = Q(description__icontains=keyword) \
            | Q(code__icontains=keyword)
        result_set = Project.objects.filter(query).order_by(
                '-date_created'
            ).distinct()
        for obj in result_set[:10]:
            results.append({
                'label': "{} - {}".format(obj.code, obj.description),
                'value': obj.code
            })
    return Response(results)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def autocomplete_titles(request):
    keyword = request.GET.get('q', '')
    results = []
    if len(keyword) > 2:
        result_set = Defect.objects.filter(reference__icontains=keyword)
        for obj in result_set.distinct()[:10]:
            results.append({
                'title': obj.reference
            })
    return Response(results)