from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from ..models import Project, Manufacturer
from .serializers import ProjectSerializer, ManufacturerSerializer

class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = LimitOffsetPagination

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    pagination_class = LimitOffsetPagination