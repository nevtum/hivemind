from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from common.models import Project

from ..domain.requests import SaveImportedDefectListRequest
from ..domain.user_stories import CommitImportDefectListUserStory
from .forms import ImportDefectsForm
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

@transaction.atomic
def complete_import(request):
    defects = request.session.get('defects', None)
    if request.method == 'POST':
        request_object = SaveImportedDefectListRequest(defects)
        response = CommitImportDefectListUserStory().execute(request_object)
        del request.session['defects']
        del request.session['project']
        if response.has_errors:
            raise ValueError(response.message)
        return redirect('defects:list')
    code = request.session.get('project', None)
    project = get_object_or_404(Project, code=code)
    res = {
        'defects': defects,
        'project': project
    }
    return render(request, 'defects/confirm_import.html', res)
