from .models import Project
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

class CreateProjectView(CreateView):
    model = Project
    template_name = 'projects/new_project.html'
    success_url=reverse_lazy('common:projects')
    fields = [
        'manufacturer',
        'code',
        'description',
        'date_created',
    ]
    
class EditProjectView(UpdateView):
    model = Project
    template_name = 'projects/edit_project.html'
    success_url=reverse_lazy('common:projects')
    fields = [
        'manufacturer',
        'code',
        'description',
        'date_created',
    ]

class ProjectListView(ListView):
    queryset = Project.objects.all().order_by('-date_created')
    template_name = 'projects/project_list.html'