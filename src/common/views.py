from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Project, Manufacturer
from .serializers import ProjectSerializer, ManufacturerSerializer

class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = LimitOffsetPagination

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    pagination_class = LimitOffsetPagination

class CreateProjectView(CreateView):
    model = Project
    template_name = 'projects/new.html'
    success_url=reverse_lazy('common:projects')
    fields = [
        'manufacturer',
        'code',
        'description',
        'date_created',
    ]
    
class EditProjectView(UpdateView):
    model = Project
    template_name = 'projects/edit.html'
    success_url=reverse_lazy('common:projects')
    fields = [
        'manufacturer',
        'code',
        'description',
        'date_created',
    ]

class ProjectListView(ListView):
    queryset = Project.objects.all().order_by('-date_created')
    template_name = 'projects/list.html'
