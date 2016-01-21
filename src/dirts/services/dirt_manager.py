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

    return Defect.objects.filter(query).order_by('-date_created')

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

def raise_dirt(**kwargs):
    defect = Defect()
    defect.project_code = kwargs['project_code']
    defect.date_created = kwargs['date_created']
    defect.submitter = kwargs['submitter']
    defect.release_id = kwargs['release_id']
    defect.status = Status.objects.get(name='Open')
    defect.priority = Priority.objects.get(id=kwargs['priority'])
    defect.reference = kwargs['reference']
    defect.description = kwargs['description']
    defect.comments = kwargs['comments']
    defect.save()
    
    event = _create_new_defect(defect.id, **kwargs)
    EventStore.append_next(event)
    return defect.id

def amend_dirt(dirt_id, **kwargs):
    # to prevent domain event from saving priority id instead of description
    event_args = dict(kwargs)
    event_args['priority'] = Priority.objects.get(id=kwargs['priority']).name
    
    defect = get_new_model(dirt_id)
    event = defect.amend(event_args['submitter'], **event_args)
    EventStore.append_next(event)

    defect = Defect.objects.get(id=dirt_id)
    defect.project_code = kwargs['project_code']
    defect.release_id = kwargs['release_id']
    defect.priority = Priority.objects.get(id=kwargs['priority'])
    defect.reference = kwargs['reference']
    defect.description = kwargs['description']
    defect.comments = kwargs['comments']
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
    
def _create_new_defect(dirt_id, **kwargs):
    priority = Priority.objects.get(pk=kwargs['priority'])
    data = {
        'project_code': kwargs['project_code'],
        'release_id': kwargs['release_id'],
        'priority': priority.name,
        'reference': kwargs['reference'],
        'description': kwargs['description'],
        'comments': kwargs['comments']
    }
    
    event = DomainEvent()
    event.sequence_nr = 0
    event.aggregate_id = dirt_id
    event.aggregate_type = 'DEFECT'
    event.event_type = DIRT_OPENED
    event.date_occurred = kwargs['date_created']
    event.username = kwargs['submitter']
    event.blob = json.dumps(data, indent=2)
    return event