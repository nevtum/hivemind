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
        defect.date_created = timezone.now()
        dirt_manager.raise_new(defect)
        return super(DefectCreateView, self).form_valid(form)

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
        defect.date_created = timezone.now()
        dirt_manager.raise_new(defect)
        return super(DefectCopyView, self).form_valid(form)

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
        return super(DefectUpdateView, self).form_valid(form)

class DefectCloseView(UpdateView):
    template_name = 'close.html'
    context_object_name = 'dirt'
    form_class = CloseDirtForm
    
    def get_object(self, request=None):
        id = self.kwargs['dirt_id']
        return dirt_manager.get_detail(id)

    def form_valid(self, form):
        defect = form.save(commit=False)
        
        # really ugly fix to get around form_valid call
        # in base class ModelFormMixin
        release_id = self.request.POST['release_id']
        reason = self.request.POST['reason']
        defect.close(release_id)
        
        dirt_manager.close_dirt(defect.id, release_id, reason, self.request.user)
        
        # bug happens after this method is called
        return super(DefectCloseView, self).form_valid(form)

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
