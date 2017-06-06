from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import dateparse, timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from taggit.models import Tag

from comments.models import Comment
from common import store as EventStore
from common.models import Project

from ..forms import (CloseDirtForm, CreateDirtForm, ReopenDirtForm, TagsForm,
                     ViewDirtReportForm)
from ..models import Defect
from ..domain.report import defect_summary
from ..mixins import DefectSearchMixin


class TagsListView(ListView):
    template_name = 'tag_list.html'
    queryset = Defect.objects.top_tags()

class DefectListView(DefectSearchMixin, ListView):
    queryset = Defect.objects.all()
    template_name = 'dirt_list.html'
    context_object_name = 'defects'
    paginate_by = 25

class ActiveDefectListView(DefectListView):
    queryset = Defect.objects.active()

class RecentlyChangedDefectListView(DefectListView):
    queryset = Defect.objects.recently_changed()

class DefectDetailView(DetailView):
    model = Defect
    context_object_name = 'model'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(DefectDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(defect__id=kwargs['object'].id)
        context['comment_count'] = comments.count()
        return context

def dirts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = Defect.objects.filter(tags__name__in=[tag.name]).distinct()
    return render(request, 'dirt_list.html', {'defects': queryset})

def time_travel(request, pk, day, month, year):
    day = int(day)
    month = int(month)
    year = int(year)
    before_date = timezone.datetime(year, month, day)
    before_date += timezone.timedelta(days=1)
    defect = get_object_or_404(Defect, pk=pk)
    return render(request, 'detail.html', { 'model': defect })

def report(request):
    if request.GET.get('project_code'):
        form = ViewDirtReportForm(request.GET)
        if form.is_valid():
            project_code = form.data['project_code']
            # need a better timezone aware datetime implementation
            freeze_date = dateparse.parse_date(form.data['prior_to_date'])
            freeze_date += timezone.timedelta(days=1)
            show_active = form.data.get('show_active_only') is not None
            project, items = defect_summary(project_code, freeze_date, show_active)
            res = {
                'form': form,
                'defects': items,
                'project': project
            }
            return render(request, 'report_request.html', res)
    else:
        form = ViewDirtReportForm()
        return render(request, 'report_request.html', { 'form': form })

@user_passes_test(lambda u: u.is_superuser)
def debug(request, pk):
    """admin specific view to inspect event sources"""
    data = {
        'stream': EventStore.get_events_for('DEFECT', pk)
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
    model = Defect

    def get_object(self, request=None):
        return super(DefectCopyView, self).get_object(request).copy()

class DefectUpdateView(UpdateView):
    model = Defect
    template_name = 'amend.html'
    context_object_name = 'dirt'
    form_class = CreateDirtForm
    
    def form_valid(self, form):
        defect = form.save(commit=False)
        defect.amend(self.request.user)
        return redirect(defect)

class DefectCloseView(UpdateView):
    model = Defect
    template_name = 'close.html'
    context_object_name = 'dirt'
    form_class = CloseDirtForm
    
    def form_valid(self, form):
        defect = form.save(commit=False)
        release_id = form.data['release_id']
        reason = form.data['reason']
        defect.close(self.request.user, release_id, reason)
        return redirect(defect)

class DefectReopenView(UpdateView):
    model = Defect
    template_name = 'reopen.html'
    context_object_name = 'dirt'
    form_class = ReopenDirtForm
    
    def form_valid(self, form):
        defect = form.save(commit=False)
        release_id = form.data['release_id']
        reason = form.data['reason']
        defect.reopen(self.request.user, release_id, reason)
        return redirect(defect)

class EditTagsView(UpdateView):
    model = Defect
    form_class = TagsForm
    context_object_name = 'dirt'
    template_name = 'edit_tags.html'

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='/login/')
def delete(request, pk):
    if request.method == 'GET':
        return render(request, 'delete_confirmation.html', {'id': pk})

    defect = Defect.objects.get(pk=pk)
    defect_model = defect.as_domainmodel()
    event = defect_model.soft_delete(request.user, timezone.now())
    EventStore.append_next(event)
    defect.delete()
    return redirect('defects:list')
