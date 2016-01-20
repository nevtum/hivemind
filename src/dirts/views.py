from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from dirts.services import dirt_manager
from dirts.forms import CreateDirtForm, ReopenDirtForm, CloseDirtForm

class DefectListView(ListView):
    template_name = 'dirt_list.html'
    context_object_name = 'defects'
    paginate_by = 25
    
    def get_queryset(self):
        search_param = self._extract_search_parameters()
        return dirt_manager.latest_dirts(search_param)
    
    def _extract_search_parameters(self):
        query = self.request.GET.get('search')
        if query:
            return query
        return ''


def detail(request, dirt_id):
    data = {
        'dirt': dirt_manager.get_new_model(dirt_id)
    }
    return render(request, 'detail.html', data)

def time_travel(request, dirt_id, day, month, year):
    day = int(day)
    month = int(month)
    year = int(year)
    before_date = timezone.datetime(year, month, day)
    before_date += timezone.timedelta(days=1)
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
        'date_created': timezone.now(),
        'submitter': request.user,
        'release_id': request.POST['release_id'],
        'priority': request.POST['priority'],
        'reference': request.POST['reference'],
        'description': request.POST['description'],
        'comments': request.POST['comments'],
    }
