from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView

from . import store as EventStore
from .models import DomainEvent, Project
from .utils import create_project_modified_dto


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
    fields = [
        'manufacturer',
        'code',
        'description',
        'date_created',
    ]

    @transaction.atomic
    def form_valid(self, form):
        project = form.save()
        seq_nr = DomainEvent.objects.belong_to('PROJECT', project.id).count()
        event = create_project_modified_dto(self.request.user, project, seq_nr)
        EventStore.append_next(event)
        return redirect('common:projects')

class ProjectListView(ListView):
    queryset = Project.objects.all()
    template_name = 'projects/list.html'
