from django.utils import timezone, dateparse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, UpdateView, CreateView
from taggit.models import Tag

from common import store as EventStore
from common.models import Project
from dirts.forms import CreateDirtForm, ReopenDirtForm, CloseDirtForm, TagsForm, ViewDirtReportForm
from dirts.models import Defect

class TagsListView(ListView):
    template_name = 'tag_list.html'
    queryset = Defect.objects.top_tags()

class DefectListView(ListView):
    template_name = 'dirt_list.html'
    context_object_name = 'defects'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Defect.objects.all()
        keyword = self.request.GET.get('search', '')
        
        if not keyword:
            return queryset
            
        query = Q(reference__icontains=keyword) \
        | Q(project_code__icontains=keyword) \
        | Q(description__icontains=keyword) \
        | Q(comments__icontains=keyword) \
        | Q(release_id__icontains=keyword) \
        | Q(tags__name__in=[keyword])
        
        return queryset.filter(query).distinct()

class ActiveDefectListView(DefectListView):
    def get_queryset(self):
        return Defect.objects.active()

class RecentlyChangedDefectListView(DefectListView):
    def get_queryset(self):
        return Defect.objects.recently_changed()

def detail(request, dirt_id):
    defect = get_object_or_404(Defect, pk=dirt_id)
    return render(request, 'detail.html', { 'model': defect })

def dirts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = Defect.objects.filter(tags__name__in=[tag.name]).distinct()
    return render(request, 'dirt_list.html', {'defects': queryset})

def time_travel(request, dirt_id, day, month, year):
    day = int(day)
    month = int(month)
    year = int(year)
    before_date = timezone.datetime(year, month, day)
    before_date += timezone.timedelta(days=1)
    defect = get_object_or_404(Defect, pk=dirt_id)
    return render(request, 'detail.html', { 'model': defect })

def _to_dto(defect, index, report_date):
    defect_model = defect.as_domainmodel(report_date)
    if defect_model.status == 'Open':
        status = 'Active'
    else:
        status = 'Closed'
    return {
        'id': index,
        'version': defect_model.release_id,
        'reference': defect_model.reference,
        'date_logged': defect_model.date_created,
        'level': defect_model.priority,
        'owner': "%s %s" % (defect.submitter.first_name, defect.submitter.last_name),
        'description': defect_model.description,
        'comments': defect_model.comments,
        'status': status
    }

def report(request):
    items = None
    project = None
    if request.GET.get('project_code'):
        form = ViewDirtReportForm(request.GET)
        if form.is_valid():
            items = []
            index = 1001
            
            # not sure if this implementation is right. Needs more testing
            before_date = dateparse.parse_date(form.data['prior_to_date'])
            before_date += timezone.timedelta(days=1)
            
            kwargs = {
                'project_code': form.data['project_code'],
                'date_created__lte': before_date,
            }
            for defect in Defect.objects.filter(**kwargs).order_by('date_created'):
                items.append(_to_dto(defect, index, before_date))
                index = index + 1
            
            if form.data.get('show_active_only') is not None:
                items = filter(lambda x: x['status'] == 'Active', items)
            
            project = get_object_or_404(Project, code=form.data['project_code'])
    else:
        form = ViewDirtReportForm()
    
    
    res = {
        'form': form,
        'defects': items,
        'project': project
    }
    return render(request, 'report_request.html', res)

@user_passes_test(lambda u: u.is_superuser)
def debug(request, dirt_id):
    """admin specific view to inspect event sources"""
    data = {
        'stream': EventStore.get_events_for('DEFECT', dirt_id)
    }
    return render(request, 'debug.html', data)

class DefectCreateView(CreateView):
    template_name = 'create.html'
    context_object_name = 'dirt'
    form_class = CreateDirtForm

    def form_valid(self, form):
        defect = form.save(commit=False)
        defect.submitter = self.request.user
        defect.raise_new()
        return redirect(defect)

class DefectCopyView(DefectCreateView, UpdateView):
    def get_object(self, request=None):
        return get_object_or_404(Defect, pk=self.kwargs['dirt_id']).copy()

class DefectUpdateView(UpdateView):
    template_name = 'amend.html'
    context_object_name = 'dirt'
    form_class = CreateDirtForm
    
    def get_object(self, request=None):
        id = self.kwargs['dirt_id']
        return get_object_or_404(Defect, pk=id)

    def form_valid(self, form):
        defect = form.save(commit=False)
        defect.amend(self.request.user)
        return redirect(defect)

class DefectCloseView(UpdateView):
    template_name = 'close.html'
    context_object_name = 'dirt'
    form_class = CloseDirtForm
    
    def get_object(self, request=None):
        id = self.kwargs['dirt_id']
        return get_object_or_404(Defect, pk=id)

    def form_valid(self, form):
        defect = form.save(commit=False)
        release_id = form.data['release_id']
        reason = form.data['reason']
        defect.close(self.request.user, release_id, reason)
        return redirect(defect)

class DefectReopenView(UpdateView):
    template_name = 'reopen.html'
    context_object_name = 'dirt'
    form_class = ReopenDirtForm
    
    def get_object(self, request=None):
        id = self.kwargs['dirt_id']
        return get_object_or_404(Defect, pk=id)

    def form_valid(self, form):
        defect = form.save(commit=False)
        release_id = form.data['release_id']
        reason = form.data['reason']
        defect.reopen(self.request.user, release_id, reason)
        return redirect(defect)

class EditTagsView(UpdateView):
    form_class = TagsForm
    context_object_name = 'dirt'
    template_name = 'edit_tags.html'

    def get_object(self, request=None):
        id = self.kwargs['dirt_id']
        return get_object_or_404(Defect, pk=id)

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='/login/')
def delete(request, dirt_id):
    if request.method == 'GET':
        return render(request, 'delete_confirmation.html', {'id': dirt_id})

    defect = Defect.objects.get(pk=dirt_id)
    defect_model = defect.as_domainmodel()
    event = defect_model.soft_delete(request.user)
    EventStore.append_next(event)
    defect.delete()
    return redirect('dirts-landing-url')
