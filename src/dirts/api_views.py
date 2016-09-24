from common import store as EventStore
from common.models import Project
from common.serializers import DomainEventSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import (api_view, detail_route,
                                       permission_classes)
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .mixins import DefectSearchMixin
from .models import Defect
from .serializers import DefectSerializer, MoreLikeThisSerializer


class DefectBaseViewSet(DefectSearchMixin, viewsets.ReadOnlyModelViewSet):
    """
    Returns a list of all defects.

    For optional search, add ?q=**[keyword]** query string to the url
    where **[keyword]** is replaced with your search parameter.
    """
    query_string_key = 'q'
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    permission_classes = (AllowAny,)

class DefectActiveViewSet(DefectBaseViewSet):
    """
    Returns a list of all **opened** defects.
    
    For optional search, add ?q=**[keyword]** query string to the url
    where **[keyword]** is replaced with your search parameter.
    """
    queryset = Defect.objects.active()

class RecentlyChangedDefectViewSet(DefectBaseViewSet):
    """
    Returns a list of all **recently changed** defects.
    
    For optional search, add ?q=**[keyword]** query string to the url
    where **[keyword]** is replaced with your search parameter.
    """
    queryset = Defect.objects.recently_changed()

@api_view(['GET'])
@permission_classes((AllowAny, ))
def more_like_this_defect(request):
    """
    Returns a list of 5 defects that are similar in content
    to the [id] specified in ?pk=[id] query string.
    """
    DEFAULT_COUNT = '5'
    id = request.GET.get('pk', '')
    if not id:
        raise ParseError("must specify an id in query string")

    count = request.GET.get('count', DEFAULT_COUNT)
    count = int(count)

    defect = get_object_or_404(Defect, pk=id)
    similar = defect.more_like_this(count)
    similar = map(lambda x: x.object, similar)

    data = {
        "current": MoreLikeThisSerializer(defect).data,
        "similar": MoreLikeThisSerializer(similar, many=True).data,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def autocomplete_projects(request):
    """
    Returns a list of max 10 projects that match the [keyword]
    specified in ?q=[keyword] query string.
    """
    keyword = request.GET.get('q', '')
    if len(keyword) <= 2:
        return Response([])

    results = []
    for obj in Project.objects.search(keyword)[:10]:
        results.append({
            'label': "{} - {}".format(obj.code, obj.description),
            'value': obj.code
        })
    return Response(results)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def autocomplete_titles(request):
    """
    Returns a list of max 10 defects where their title
    matches the [keyword] specified in ?q=[keyword] query string.
    """
    keyword = request.GET.get('q', '')
    if len(keyword) <= 2:
        return Response([])

    result_set = Defect.objects.filter(reference__icontains=keyword)
    result_set = result_set.distinct()
    result_set = map(lambda x: {'title' : x.reference}, result_set[:10])
    return Response(list(result_set))
