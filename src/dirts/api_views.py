import json
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
        result_set = Defect.objects.filter(reference__icontains=keyword)
        for obj in result_set.distinct()[:10]:
            results.append({
                'title': obj.reference
            })
    return HttpResponse(json.dumps(results), content_type='application/json')