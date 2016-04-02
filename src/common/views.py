from .models import Project
from django.views.generic import ListView, UpdateView, CreateView

class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'