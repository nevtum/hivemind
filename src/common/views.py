from .models import Project
from django.views.generic import ListView, UpdateView, CreateView

class ProjectListView(ListView):
    queryset = Project.objects.all().order_by('-date_created')
    template_name = 'project_list.html'