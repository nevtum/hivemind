from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, detail_route,
                                       permission_classes)
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common import store as EventStore
from common.models import Project

from ..mixins import DefectSearchMixin
from ..models import Defect, Priority, Status
from .serializers import (CreateDefectSerializer, DefectSerializer,
                          MoreLikeThisSerializer, PrioritySerializer,
                          StatusSerializer, SuggestionSerializer)


class PriorityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Priority.objects.all()
    paginator = None
    permission_classes = (AllowAny,)
    serializer_class = PrioritySerializer

class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Status.objects.all()
    paginator = None
    permission_classes = (AllowAny,)
    serializer_class = StatusSerializer

class CreateDefectView(generics.CreateAPIView):
    serializer_class = CreateDefectSerializer

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user)

class DefectBaseViewSet(DefectSearchMixin, viewsets.ReadOnlyModelViewSet):
    """
    Returns a list of all defects.

    For optional search, add ?q=**[keyword]** query string to the url
    where **[keyword]** is replaced with your search parameter.
    """
    query_string_key = 'q'
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        events = EventStore.get_events_for('DEFECT', instance.id)
        return Response(events)


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
def more_like_this_defect(request, pk):
    """
    Returns a list of 5 to a maximum of 20 defects that are similar
    in content to the pk specified.
    
    Set the optional query string ?count to show a custom number of
    similar items.
    """
    DEFAULT_COUNT = '5'

    count = request.GET.get('count', DEFAULT_COUNT)
    count = int(count)

    MAX_COUNT = 20
    if count > MAX_COUNT:
        count = MAX_COUNT

    defect = get_object_or_404(Defect, pk=pk)
    similar = defect.more_like_this(count)

    data = {
        "current": MoreLikeThisSerializer(
            defect,
            context={'request': request}
        ).data,
        "similar": MoreLikeThisSerializer(
            similar,
            many=True,
            context={'request': request}
        ).data,
    }
    return Response(data)

class AutoCompleteProjects(viewsets.ReadOnlyModelViewSet):
    """
    Returns a list of max 10 projects that match the [keyword]
    specified in ?q=[keyword] query string.
    """
    serializer_class = SuggestionSerializer
    permission_classes = (AllowAny,)
    paginator = None

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        if len(keyword) <= 2:
            return []

        results = []
        for obj in Project.objects.search(keyword)[:10]:
            results.append({
                'label': "{} - {}".format(obj.code, obj.description),
                'value': obj.code
            })
        return results

class AutoCompleteDefectTitles(viewsets.ReadOnlyModelViewSet):
    """
    Returns a list of max 10 defects where their title
    matches the [keyword] specified in ?q=[keyword] query string.
    """
    serializer_class = SuggestionSerializer
    permission_classes = (AllowAny,)
    paginator = None

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        if len(q) <= 2:
            return []
        else:
            return Defect.objects.filter(reference__icontains=q)[:10]
