from rest_framework import viewsets

from ..models import Manufacturer, Project
from .pagination import CustomLimitOffsetPagination
from .serializers import ManufacturerSerializer, ProjectSerializer


class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomLimitOffsetPagination

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    pagination_class = CustomLimitOffsetPagination
