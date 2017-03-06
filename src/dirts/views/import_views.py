from common.models import Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ImportDirtsForm
from ..utils import import_data


@login_required(login_url='/login/')
def begin_import(request):
    if request.method == 'POST':
        form = ImportDirtsForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['project'] = form.cleaned_data['project_code']
            request.session['defects'] = import_data(form.cleaned_data['import_file'])
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
    res = {
        'defects': defects,
        'project': project
    }
    return render(request, 'confirm_import.html', res)
