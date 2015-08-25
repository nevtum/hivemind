from .models import Defect
from rest_framework import viewsets, generics
from . import serializers

class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = serializers.DefectSerializer
