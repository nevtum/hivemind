from common import store as EventStore
from common.models import Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..constants import DIRT_IMPORTED
from ..forms import ImportDirtsForm
from ..serializers import ImportDefectSerializer
from ..utils import import_data


@login_required(login_url='/login/')
def begin_import(request):
    if request.method == 'POST':
        form = ImportDirtsForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['project'] = form.cleaned_data['project_code']
            request.session['defects'] = import_data(request)
            return redirect('complete-import')
        else:
            return render(request, 'begin_import.html', {'form': form})
    form = ImportDirtsForm()
    return render(request, 'begin_import.html', {'form': form})

@login_required(login_url='/login/')
def complete_import(request):
    defects = request.session.get('defects', None)
    code = request.session.get('project', None)
    project = get_object_or_404(Project, code=code)
    if request.method == 'POST':
        for json in defects:
            serializer = ImportDefectSerializer(data=json)
            if serializer.is_valid():
                defect = serializer.save()
                event = {
                    'sequence_nr': 0,
                    'aggregate_id': defect.id,
                    'aggregate_type': 'DEFECT',
                    'event_type': DIRT_IMPORTED,
                    'created': defect.date_created,
                    'created_by': defect.submitter,
                    'payload': {
                        'project_code': defect.project_code,
                        'release_id': defect.release_id,
                        'status': defect.status.name,
                        'priority': defect.priority.name,
                        'reference': defect.reference,
                        'description': defect.description,
                        'comments': defect.comments
                    }
                }
                EventStore.append_next(event)
        return redirect('dirts-list')
    res = {
        'defects': defects,
        'project': project
    }
    return render(request, 'confirm_import.html', res)
