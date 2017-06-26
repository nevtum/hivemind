
from django.shortcuts import get_object_or_404

from common.models import Project, DomainEvent

from ..models import Defect


# def _to_dto(index, defect, end_date):
#     defect_model = defect.as_domainmodel(end_date)
#     owner = '{} {}'.format(defect.submitter.first_name, defect.submitter.last_name)
#     if defect_model.status == 'Open':
#         status = 'Active'
#     else:
#         status = 'Closed'
        
#     return {
#         'id': index + 1001,
#         'version': defect_model.release_id,
#         'reference': defect_model.reference,
#         'date_logged': defect_model.date_created,
#         'level': defect_model.priority,
#         'owner': owner,
#         'description': defect_model.description,
#         'comments': defect_model.comments,
#         'status': status
#     }

# def defect_summary_old(project_code, end_date, show_active=True):
#     project = get_object_or_404(Project, code=project_code)
#     queryset = Defect.objects.filter(
#         project_code=project_code,
#         date_created__lte=end_date
#     ).order_by('date_created')
#     items = [_to_dto(index, defect, end_date) for index, defect in enumerate(queryset)]

#     if show_active:
#         return project, filter(lambda x: x['status'] == 'Active', items)
#     else:
#         return project, items

def defect_summary(project_code, end_date, show_active=True):
    # return defect_summary_old(project_code, end_date, show_active)
    return _defect_summary_new(project_code, end_date, show_active)

from common.api.serializers import DomainEventReadSerializer
from itertools import groupby
from django.contrib.contenttypes.models import ContentType
from ..domain.models import DefectViewModel

def _defect_summary_new(project_code, end_date, show_active=True):
    events = _get_events(project_code, end_date)

    items = []    
    for event_dtos in _grouped_by_aggregate_id(events):
        items.append(_to_item(event_dtos))

    project = get_object_or_404(Project, code=project_code)

    if show_active:
        print('here')
        return project, filter(lambda x: x['status'] == 'Active', items)
    else:
        return project, items

def _grouped_by_aggregate_id(events):
    event_groups = groupby(events, lambda e: e.aggregate_id)
    for aggregate_id, group in event_groups:
        event_dtos = []
        for event in group:
            assert(aggregate_id == event.aggregate_id)
            event_dto = DomainEventReadSerializer(event).data
            event_dtos.append(event_dto)
        yield event_dtos

def _get_events(project_code, end_date):
    defect_ids = Defect.objects.filter(project_code=project_code).values('id')
    events = DomainEvent.objects.order_by('aggregate_id', 'sequence_nr')
    events = events.select_related('owner')
    events = events.filter(
        aggregate_type='DEFECT',
        aggregate_id__in=defect_ids,
        date_occurred__lte=end_date
    )
    return events

def _to_item(event_dtos):
    defect_model = DefectViewModel(event_dtos)

    if defect_model.status == 'Open':
        status = 'Active'
    elif defect_model.status == 'Obsolete':
        status = 'Obsolete'
    else:
        status = 'Closed'
        
    return {
        'id': defect_model.id,
        'version': defect_model.release_id,
        'reference': defect_model.reference,
        'date_logged': defect_model.date_created,
        'level': defect_model.priority,
        'owner': defect_model.submitter,
        'description': defect_model.description,
        'comments': defect_model.comments,
        'status': status
    }