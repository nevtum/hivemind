from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, CreateView

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

class ActiveDefectListView(DefectListView):
    def get_queryset(self):
        return dirt_manager.active_dirts()

class RecentlyChangedDefectListView(DefectListView):
    def get_queryset(self):
        return dirt_manager.recently_changed()

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

class DefectCreateView(CreateView):
    template_name = 'create.html'
    context_object_name = 'dirt'
    form_class = CreateDirtForm

    def form_valid(self, form):
        defect = form.save(commit=False)
        defect.submitter = self.request.user
        id = dirt_manager.raise_new(defect)
        assert(id == defect.id)
        return redirect('dirt-detail-url', defect.id)

class DefectCopyView(UpdateView):
    template_name = 'create.html'
    context_object_name = 'dirt'
    form_class = CreateDirtForm
    
    def get_object(self, request=None):
        id = self.kwargs['dirt_id']
        return dirt_manager.get_copy(id)

    def form_valid(self, form):
        defect = form.save(commit=False)
        defect.submitter = self.request.user
        id = dirt_manager.raise_new(defect)
        assert(id == defect.id)
        return redirect('dirt-detail-url', defect.id)

class DefectUpdateView(UpdateView):
    template_name = 'amend.html'
    context_object_name = 'dirt'
    form_class = CreateDirtForm
    
    def get_object(self, request=None):
        id = self.kwargs['dirt_id']
        return dirt_manager.get_detail(id)

    def form_valid(self, form):
        defect = form.save(commit=False)
        dirt_manager.amend(defect)
        return redirect('dirt-detail-url', defect.id)

class DefectCloseView(UpdateView):
    template_name = 'close.html'
    context_object_name = 'dirt'
    form_class = CloseDirtForm
    
    def get_object(self, request=None):
        id = self.kwargs['dirt_id']
        return dirt_manager.get_detail(id)

    def form_valid(self, form):
        defect = form.save(commit=False)
        release_id = form.data['release_id']
        reason = form.data['reason']
        dirt_manager.close_dirt(defect.id, release_id, reason, self.request.user)
        return redirect('dirt-detail-url', defect.id)

class DefectReopenView(UpdateView):
    template_name = 'reopen.html'
    context_object_name = 'dirt'
    form_class = ReopenDirtForm
    
    def get_object(self, request=None):
        id = self.kwargs['dirt_id']
        return dirt_manager.get_detail(id)

    def form_valid(self, form):
        defect = form.save(commit=False)
        release_id = form.data['release_id']
        reason = form.data['reason']
        dirt_manager.reopen(defect.id, self.request.user, release_id, reason)
        return redirect('dirt-detail-url', defect.id)

@login_required(login_url='/login/')
def delete(request, dirt_id):
    if request.method == 'GET':
        return render(request, 'delete_confirmation.html', {'id': dirt_id})

    # otherwise post
    dirt_manager.delete_dirt(dirt_id, request.user)
    return redirect('dirts-landing-url')
