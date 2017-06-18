
from django.shortcuts import get_object_or_404

from common.models import Project, DomainEvent

from ..models import Defect


def _to_dto(index, defect, end_date):
    defect_model = defect.as_domainmodel(end_date)
    owner = '{} {}'.format(defect.submitter.first_name, defect.submitter.last_name)
    if defect_model.status == 'Open':
        status = 'Active'
    else:
        status = 'Closed'
        
    return {
        'id': index + 1001,
        'version': defect_model.release_id,
        'reference': defect_model.reference,
        'date_logged': defect_model.date_created,
        'level': defect_model.priority,
        'owner': owner,
        'description': defect_model.description,
        'comments': defect_model.comments,
        'status': status
    }

def defect_summary_old(project_code, end_date, show_active=True):
    project = get_object_or_404(Project, code=project_code)
    queryset = Defect.objects.filter(
        project_code=project_code,
        date_created__lte=end_date
    ).order_by('date_created')
    items = [_to_dto(index, defect, end_date) for index, defect in enumerate(queryset)]

    if show_active:
        return project, filter(lambda x: x['status'] == 'Active', items)
    else:
        return project, items

def defect_summary(project_code, end_date, show_active=True):
    return defect_summary_old(project_code, end_date, show_active=True)
    # return defect_summary_new(project_code, end_date, show_active=True)

def defect_summary_new(project_code, end_date, show_active=True):
    events = get_events(project_code, end_date)
    
    for event_dtos in grouped_by_object_id(events):
        import pdb; pdb.set_trace()

    project = get_object_or_404(Project, code=project_code)
    return project, []

def grouped_by_object_id(events):
    from itertools import groupby
    event_groups = groupby(events, lambda e: e.object_id)
    for object_id, group in event_groups:
        event_dtos = []
        for event in group:
            assert(object_id == event.object_id)
            event_dto = to_item(event)
            event_dtos.append(event_dto)
        yield cleaned

def get_events(project_code, end_date):
    from django.contrib.contenttypes.models import ContentType
    defect_ids = Defect.objects.filter(project_code=project_code).values('id')
    events = DomainEvent.objects.filter(
        content_type=ContentType.objects.get(model='defect'),
        object_id__in=defect_ids,
        date_occurred__lte=end_date
    )
    events = events.select_related('owner')
    return events