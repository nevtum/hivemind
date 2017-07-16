from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import dateparse, timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from taggit.models import Tag

from comments.models import Comment
from common import store as EventStore
from common.models import Project

from ..domain.report import defect_summary
from ..domain.requests import MutateDefectRequest
from ..domain.user_stories import (CloseDefectUserStory, CreateDefectUserStory,
                                   LockDefectUserStory, UpdateDefectUserStory)
from ..forms import (CloseDefectForm, CreateDefectForm, DefectSummaryForm,
                     LockDefectForm, ReopenDefectForm, TagsForm)
from ..mixins import DefectSearchMixin
from ..models import Defect


class TagsListView(ListView):
    template_name = 'defects/tags.html'
    queryset = Defect.objects.top_tags()

class DefectListView(DefectSearchMixin, ListView):
    queryset = Defect.objects.all()
    template_name = 'defects/list.html'
    context_object_name = 'defects'
    paginate_by = 25

class ActiveDefectListView(DefectListView):
    queryset = Defect.objects.active()

class RecentlyChangedDefectListView(DefectListView):
    queryset = Defect.objects.recently_changed()

class DefectDetailView(DetailView):
    model = Defect
    context_object_name = 'model'
    template_name = 'defects/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DefectDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(defect__id=kwargs['object'].id)
        context['comment_count'] = comments.count()
        return context

def defects_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = Defect.objects.filter(tags__name__in=[tag.name]).distinct()
    return render(request, 'defects/list.html', {'defects': queryset})

def time_travel(request, pk, day, month, year):
    day = int(day)
    month = int(month)
    year = int(year)
    # view appears to be broken
    end_date = timezone.datetime(year, month, day)
    end_date += timezone.timedelta(days=1)
    defect = get_object_or_404(Defect, pk=pk)
    return render(request, 'defects/detail.html', { 'model': defect })

def report(request):
    if request.GET.get('project_code'):
        form = DefectSummaryForm(request.GET)
        if form.is_valid():
            project_code = form.data['project_code']
            # need a better timezone aware datetime implementation
            end_date = dateparse.parse_date(form.data['end_date'])
            end_date += timezone.timedelta(days=1)
            show_active = form.data.get('show_active_only') is not None
            project, items = defect_summary(project_code, end_date, show_active)
            res = {
                'form': form,
                'defects': items,
                'project': project
            }
            return render(request, 'defects/summary.html', res)
        else:
            # to refactor later
            raise Exception("Must specify end_date")
    else:
        form = DefectSummaryForm()
        return render(request, 'defects/summary.html', { 'form': form })

@user_passes_test(lambda u: u.is_superuser)
def debug(request, pk):
    """admin specific view to inspect event sources"""
    instance = Defect.objects.get(pk=pk)
    data = {
        'stream': EventStore.get_events_for('DEFECT', instance.id)
    }
    return render(request, 'defects/debug.html', data)

class DefectCreateView(CreateView):
    template_name = 'defects/create.html'
    form_class = CreateDefectForm

    def form_valid(self, form):
        request_object = MutateDefectRequest(self.request.user, form)
        response = CreateDefectUserStory().execute(request_object)
        if response.has_errors:
            raise ValueError(response.message)
        return redirect(response.value)

    # def form_valid(self, form):
    #     defect = form.save(commit=False)
    #     defect.submitter = self.request.user
    #     defect.save()
    #     return redirect(defect)

class DefectCopyView(DefectCreateView, UpdateView):
    model = Defect

    def get_object(self, request=None):
        return super(DefectCopyView, self).get_object(request).copy()

class DefectUpdateView(UpdateView):
    model = Defect
    template_name = 'defects/amend.html'
    form_class = CreateDefectForm
    
    def form_valid(self, form):
        request_object = MutateDefectRequest(self.request.user, form)
        response = UpdateDefectUserStory().execute(request_object)
        if response.has_errors:
            raise ValueError(response.message)
        return redirect(response.value)

    # def form_valid(self, form):
    #     defect = form.save(commit=False)
    #     defect.amend(self.request.user)
    #     return redirect(defect)

class DefectCloseView(UpdateView):
    model = Defect
    template_name = 'defects/close.html'
    form_class = CloseDefectForm
    
    def form_valid(self, form):
        request_object = MutateDefectRequest(self.request.user, form)
        response = CloseDefectUserStory().execute(request_object)
        if response.has_errors:
            raise ValueError(response.message)
        return redirect(response.value)

    # def form_valid(self, form):
    #     defect = form.save(commit=False)
    #     release_id = form.cleaned_data['release_id']
    #     reason = form.cleaned_data['reason']
    #     defect.close(self.request.user, release_id, reason)
    #     return redirect(defect)

class DefectLockView(UpdateView):
    model = Defect
    template_name = 'defects/lock.html'
    form_class = LockDefectForm

    def form_valid(self, form):
        request_object = MutateDefectRequest(self.request.user, form)
        response = LockDefectUserStory().execute(request_object)
        if response.has_errors:
            raise ValueError(response.message)
        return redirect(response.value)

    # def form_valid(self, form):
    #     defect = form.instance
    #     kwargs = form.cleaned_data
    #     kwargs['user'] = self.request.user
    #     kwargs['timestamp'] = timezone.now()
    #     defect_model = defect.as_domainmodel()
    #     event = defect_model.make_obsolete(**kwargs)
    #     EventStore.append_next(event)
    #     return redirect(defect)

class DefectReopenView(UpdateView):
    model = Defect
    template_name = 'defects/reopen.html'
    form_class = ReopenDefectForm
    
    def form_valid(self, form):
        defect = form.save(commit=False)
        release_id = form.data['release_id']
        reason = form.data['reason']
        defect.reopen(self.request.user, release_id, reason)
        return redirect(defect)

class EditTagsView(UpdateView):
    model = Defect
    form_class = TagsForm
    context_object_name = 'defect'
    template_name = 'defects/edit_tags.html'

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='/login/')
def delete(request, pk):
    if request.method == 'GET':
        return render(request, 'defects/confirm_delete.html', {'id': pk})

    defect = Defect.objects.get(pk=pk)
    defect_model = defect.as_domainmodel()
    event = defect_model.soft_delete(request.user, timezone.now())
    EventStore.append_next(event)
    defect.delete()
    return redirect('defects:list')
