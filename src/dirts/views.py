from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from dirts.services import dirt_manager
from dirts.forms import CreateDirtForm

def index(request):
    search_param = _extract_search_parameters(request)
    defects = dirt_manager.latest_dirts(search_param)
    return render(request, 'dirt_list.html', {'defects': defects})

def detail(request, dirt_id):
    data = {
        'dirt': dirt_manager.get_detail(dirt_id),
        'history': dirt_manager.get_history(dirt_id),
    }
    return render(request, 'detail.html', data)

@login_required(login_url='/login/')
def create(request):
    if request.method == 'GET':
        form = CreateDirtForm()
        return render(request, 'create.html', {'form': form})

    # otherwise post
    args = _create_args(request)
    dirt_manager.raise_dirt(**args)
    return redirect('dirts-landing-url')

@login_required(login_url='/login/')
def amend(request, dirt_id):
    if request.method == 'GET':
        summary = dirt_manager.get_detail(dirt_id)
        form = CreateDirtForm(instance=summary)
        return render(request, 'amend.html', {'form': form, 'dirt': summary})

    # otherwise post
    args = _create_args(request)
    dirt_manager.amend_dirt(dirt_id, **args)
    return redirect('dirt-detail-url', dirt_id)

@login_required(login_url='/login/')
def close(request, dirt_id):
    # Very basic functionality for now
    # To add confirmation screen if not marked accepted/rejected.
    dirt_manager.close_dirt(dirt_id, request.user)
    return redirect('dirt-detail-url', dirt_id)

@login_required(login_url='/login/')
def delete(request, dirt_id):
    if request.method == 'GET':
        return render(request, 'delete_confirmation.html', {'id': dirt_id})

    # otherwise post
    dirt_manager.delete_dirt(dirt_id)
    return redirect('dirts-landing-url')

def _create_args(request):
    return {
        'project_code': request.POST['project_code'],
        'date_created': datetime.utcnow(),
        'submitter': request.user,
        'release_id': request.POST['release_id'],
        'priority': request.POST['priority'],
        'reference': request.POST['reference'],
        'description': request.POST['description'],
        'comments': request.POST['comments'],
    }

def _extract_search_parameters(request):
    query = request.GET.get('search')
    if query:
        return query
    return ''
