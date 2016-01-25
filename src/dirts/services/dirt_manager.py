import json
from django.db.models import Q

from common.models import DomainEvent
from common import store as EventStore
from dirts.domain.models import DefectViewModel
from dirts.models import Defect, Status, Priority
from dirts.constants import (DIRT_OPENED, DIRT_REOPENED, 
DIRT_AMENDED, DIRT_CLOSED, DIRT_DELETED)

def latest_dirts(keyword):
    query = Q(reference__icontains=keyword) \
    | Q(project_code__icontains=keyword) \
    | Q(description__icontains=keyword) \
    | Q(comments__icontains=keyword) \
    | Q(release_id__icontains=keyword)

    return Defect.objects.latest().filter(query)

def active_dirts():
    return Defect.objects.active()

def get_new_model(dirt_id):
    events = EventStore.get_events_for('DEFECT', dirt_id)
    return DefectViewModel(events)

def get_historic_dirt(dirt_id, before_date):
    events = EventStore.get_events_for('DEFECT', dirt_id, before_date)
    return DefectViewModel(events)
    
def get_detail(dirt_id):
    return Defect.objects.get(pk=dirt_id)

def get_copy(dirt_id):
    defect = get_detail(dirt_id)
    copy = Defect()
    copy.project_code = defect.project_code
    copy.release_id = defect.release_id
    return copy

def raise_new(defect):
    defect.save()
    event = _create_event_from(defect)
    EventStore.append_next(event)

def amend(defect):
    defect_aggregate = get_new_model(defect.id)
    event = defect_aggregate.amend(defect.submitter, **_to_kwargs(defect))
    EventStore.append_next(event)
    defect.save()

def reopen(dirt_id, user, release_id, reason):
    defect = get_new_model(dirt_id)
    event = defect.reopen(user, release_id, reason)
    EventStore.append_next(event)
    
    defect = Defect.objects.get(id=dirt_id)
    defect.reopen(release_id)
    
def close_dirt(dirt_id, release_id, reason, user):
    defect = get_new_model(dirt_id)
    event = defect.close(user, release_id, reason)
    EventStore.append_next(event)
    
    defect = Defect.objects.get(id=dirt_id)
    defect.close(release_id)

def delete_dirt(dirt_id, user):
    defect = get_new_model(dirt_id)
    event = defect.soft_delete(user)
    EventStore.append_next(event)
    
    Defect.objects.get(id=dirt_id).delete()

def _to_kwargs(defect):
    return dict({
        'project_code': defect.project_code,
        'date_created': defect.date_created,
        'submitter': defect.submitter,
        'release_id': defect.release_id,
        'status': defect.status,
        'priority': defect.priority.name,
        'reference': defect.reference,
        'description': defect.description,
        'comments': defect.comments,
    })

def _create_event_from(defect):
    data = {
        'project_code': defect.project_code,
        'release_id': defect.release_id,
        'priority': defect.priority.name,
        'reference': defect.reference,
        'description': defect.description,
        'comments': defect.comments
    }
    
    event = DomainEvent()
    event.sequence_nr = 0
    event.aggregate_id = defect.id
    event.aggregate_type = 'DEFECT'
    event.event_type = DIRT_OPENED
    event.date_occurred = defect.date_created
    event.username = defect.submitter
    event.blob = json.dumps(data, indent=2)
    return event