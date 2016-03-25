import json
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import viewsets, generics
from .models import Defect
from . import serializers

class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = serializers.DefectSerializer

def autocomplete(request):
    keyword = request.GET.get('q', '')
    results = []
    if len(keyword) > 2:
        query = Q(reference__icontains=keyword) \
        | Q(project_code__icontains=keyword) \
        | Q(description__icontains=keyword) \
        | Q(comments__icontains=keyword) \
        | Q(release_id__icontains=keyword) \
        | Q(tags__name__in=[keyword])
        
        result_set = Defect.objects.filter(query).distinct()[:10]
        for obj in result_set:
            results.append({
                'title': obj.reference
            })
    return HttpResponse(json.dumps(results), content_type='application/json')