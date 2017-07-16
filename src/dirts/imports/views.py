from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from common import store as EventStore
from common.models import Project

from .forms import ImportDefectsForm
from .serializers import ImportDefectSerializer
from .utils import import_data
from dirts.utils import create_import_event_dto
from dirts.models import Status

def get_closed_date(json_data):
    serializer = ImportDefectSerializer(data=json_data)
    if serializer.is_valid():
        return serializer.validated_data['date_changed']

def persist_closed_defect(json_data):
    updated_data = json_data.copy()
    updated_data['status'] = 'Open'
    date_closed = get_closed_date(updated_data)
    defect = persist_open_defect(updated_data)
    user = defect.submitter
    release_id = defect.release_id
    model = defect.as_domainmodel()
    event = model.close(user, release_id, '', date_closed)
    EventStore.append_next(event)
    defect.status = Status.objects.get(name='Closed')
    defect.release_id = release_id
    defect.save()

def persist_open_defect(json_data):
    serializer = ImportDefectSerializer(data=json_data)
    if not serializer.is_valid():
        raise Exception("Something went wrong with import!")
    defect = serializer.save()
    event = create_import_event_dto(defect)
    EventStore.append_next(event)
    return defect

def persist_to_database(json_data):
    if json_data['status'] == 'Closed':
        persist_closed_defect(json_data)
    else:
        persist_open_defect(json_data)

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

@transaction.atomic
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
