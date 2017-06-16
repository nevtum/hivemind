from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from .models import Project

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
