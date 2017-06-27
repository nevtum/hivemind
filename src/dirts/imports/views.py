from django.shortcuts import get_object_or_404, redirect, render

from common import store as EventStore
from common.models import Project

from ..constants import DEFECT_IMPORTED
from .forms import ImportDefectsForm
from .serializers import ImportDefectSerializer
from .utils import import_data


def begin_import(request):
    if request.method == 'POST':
        form = ImportDefectsForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['project'] = form.cleaned_data['project_code']
            request.session['defects'] = import_data(request)
            return redirect('defects:imports:complete-import')
        else:
            return render(request, 'defects/begin_import.html', {'form': form})
    form = ImportDefectsForm()
    return render(request, 'defects/begin_import.html', {'form': form})

def import_event(defect):
    return {
        'sequence_nr': 0,
        'aggregate_id': defect.id,
        'aggregate_type': 'defect',
        'event_type': DEFECT_IMPORTED,
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

def get_closed_date(json_data):
    serializer = ImportDefectSerializer(data=json_data)
    if serializer.is_valid():
        return serializer.validated_data['date_changed']

def persist_closed_defect(json_data):
    updated_data = json_data.copy()
    updated_data['status'] = 'Open'
    closed_date = get_closed_date(updated_data)
    defect = persist_open_defect(updated_data)
    defect.import_close(closed_date)

def persist_open_defect(json_data):
    serializer = ImportDefectSerializer(data=json_data)
    if not serializer.is_valid():
        raise Exception("Something went wrong with import!")
    defect = serializer.save()

    ## Broke this functionality for now
    ## since a handler is listinging on the
    ## Defect created signal and automatically
    ## creates a defect opened event. Therefore
    ## a optimistic concurrency error occurs.
    # imported_event = import_event(defect)
    # EventStore.append_next(imported_event)
    return defect

def persist_to_database(json_data):
    if json_data['status'] == 'Closed':
        persist_closed_defect(json_data)
    else:
        persist_open_defect(json_data)

def complete_import(request):
    defects = request.session.get('defects', None)
    code = request.session.get('project', None)
    project = get_object_or_404(Project, code=code)
    if request.method == 'POST':
        for json in defects:
            persist_to_database(json)
        del request.session['defects']
        del request.session['project']
        return redirect('defects:list')
    res = {
        'defects': defects,
        'project': project
    }
    return render(request, 'defects/confirm_import.html', res)
