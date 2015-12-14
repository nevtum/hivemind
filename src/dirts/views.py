import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from dirts.services import dirt_manager
from dirts.forms import CreateDirtForm, ReopenDirtForm, CloseDirtForm

def index(request):
    page_nr = _extract_page_nr(request)
    search_param = _extract_search_parameters(request)
    defects = dirt_manager.latest_dirts(search_param)
    viewmodel = Paginator(defects, 25).page(page_nr)
    
    return render(request, 'dirt_list.html', {'defects': viewmodel})

def detail(request, dirt_id):
    data = {
        'dirt': dirt_manager.get_new_model(dirt_id)
    }
    return render(request, 'detail.html', data)

def time_travel(request, dirt_id, day, month, year):
    day = int(day)
    month = int(month)
    year = int(year)
    before_date = datetime.date(year, month, day)
    before_date += datetime.timedelta(days=1)
    data = {
        'dirt': dirt_manager.get_historic_dirt(dirt_id, before_date)
    }
    return render(request, 'detail.html', data)

@login_required(login_url='/login/')
def create(request):
    if request.method == 'GET':
        form = CreateDirtForm()
        return render(request, 'create.html', {'form': form})

    # otherwise post
    form = CreateDirtForm(request.POST)
    if not form.is_valid():
        return render(request, 'create.html', {'form': form})

    args = _create_args(request)
    dirt_id = dirt_manager.raise_dirt(**args)
    return redirect('dirt-detail-url', dirt_id)

@login_required(login_url='/login/')
def copy(request, dirt_id):
    if request.method == 'GET':
        dirt = dirt_manager.get_copy(dirt_id)
        form = CreateDirtForm(instance=dirt)
        return render(request, 'create.html', {'form': form})

    # otherwise post
    form = CreateDirtForm(request.POST)
    if not form.is_valid():
        return render(request, 'create.html', {'form': form})

    args = _create_args(request)
    dirt_id = dirt_manager.raise_dirt(**args)
    return redirect('dirt-detail-url', dirt_id)

@login_required(login_url='/login/')
def amend(request, dirt_id):
    dirt = dirt_manager.get_detail(dirt_id)
    if request.method == 'GET':
        form = CreateDirtForm(instance=dirt)
        return render(request, 'amend.html', {'form': form, 'dirt': dirt})

    # otherwise post
    form = CreateDirtForm(request.POST)
    if not form.is_valid():
        return render(request, 'amend.html', {'form': form, 'dirt': dirt})

    args = _create_args(request)
    dirt_manager.amend_dirt(dirt_id, **args)
    return redirect('dirt-detail-url', dirt_id)

@login_required(login_url='/login/')
def close(request, dirt_id):
    dirt = dirt_manager.get_detail(dirt_id)
    if request.method == 'GET':
        form = CloseDirtForm(instance=dirt)
        return render(request, 'close.html', {'form': form, 'dirt': dirt})
    
    # otherwise post
    form = CloseDirtForm(request.POST)
    if not form.is_valid():
        return render(request, 'close.html', {'form': form, 'dirt': dirt})
    
    reason = request.POST['reason']
    release_id = request.POST['release_id']
    
    dirt_manager.close_dirt(dirt_id, release_id, reason, request.user)
    return redirect('dirt-detail-url', dirt_id)

@login_required(login_url='/login/')
def reopen(request, dirt_id):
    dirt = dirt_manager.get_detail(dirt_id)
    if request.method == 'GET':
        form = ReopenDirtForm(instance=dirt)
        return render(request, 'reopen.html', {'form': form, 'dirt': dirt})

    # otherwise post
    form = ReopenDirtForm(request.POST)
    if not form.is_valid():
        return render(request, 'reopen.html', {'form': form, 'dirt': dirt})

    release_id = request.POST['release_id']
    reason = request.POST['reason']
    dirt_manager.reopen(dirt_id, request.user, release_id, reason)
    return redirect('dirt-detail-url', dirt_id)

@login_required(login_url='/login/')
def delete(request, dirt_id):
    if request.method == 'GET':
        return render(request, 'delete_confirmation.html', {'id': dirt_id})

    # otherwise post
    dirt_manager.delete_dirt(dirt_id, request.user)
    return redirect('dirts-landing-url')

def _create_args(request):
    return {
        'project_code': request.POST['project_code'],
        'date_created': datetime.datetime.now(),
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

def _extract_page_nr(request):
    page_nr = request.GET.get('page')
    if page_nr:
        return page_nr
    return 1
