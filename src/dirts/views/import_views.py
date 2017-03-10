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

def import_event(defect):
    return {
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

# man this is ugly!
def get_closed_date(json_data):
    serializer = ImportDefectSerializer(data=json_data)
    if serializer.is_valid():
        return serializer.validated_data['date_changed']

def persist_closed_defect(json_data):
    updated_data = json_data.copy()
    updated_data['status'] = 'Open'
    closed_date = get_closed_date(updated_data)
    defect = persist_open_defect(updated_data)
    defect.close_at(closed_date)

def persist_open_defect(json_data):
    serializer = ImportDefectSerializer(data=json_data)
    if not serializer.is_valid():
        raise Exception("Something went wrong with import!")
    defect = serializer.save()
    imported_event = import_event(defect)
    EventStore.append_next(imported_event)
    return defect

def persist_to_database(json_data):
    if json_data['status'] == 'Closed':
        persist_closed_defect(json_data)
    else:
        persist_open_defect(json_data)

@login_required(login_url='/login/')
def complete_import(request):
    defects = request.session.get('defects', None)
    code = request.session.get('project', None)
    project = get_object_or_404(Project, code=code)
    if request.method == 'POST':
        for json in defects:
            persist_to_database(json)
        return redirect('dirts-list')
    res = {
        'defects': defects,
        'project': project
    }
    return render(request, 'confirm_import.html', res)
