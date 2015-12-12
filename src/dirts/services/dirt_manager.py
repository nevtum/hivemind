import json
from django.utils import timezone
from django.db.models import Q

from common.models import DomainEvent
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
    events = get_history(dirt_id)
    return DefectViewModel(events)

def get_detail(dirt_id):
    return Defect.objects.get(pk=dirt_id)

def get_history(dirt_id):
    return DomainEvent.objects.filter(aggregate_type='DEFECT', aggregate_id=dirt_id).order_by('-date_occurred')

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
    
    data = {
        'project_code': defect.project_code,
        'release_id': defect.release_id,
        'priority': defect.priority.name,
        'reference': defect.reference,
        'description': defect.description,
        'comments': defect.comments
    }
    
    _save_event(DIRT_OPENED, defect.id, defect.date_created, defect.submitter.username, data)

    return defect.id

def amend_dirt(dirt_id, **kwargs):
    defect = Defect.objects.get(id=dirt_id)

    if defect.status.name != "Open":
        raise Exception("DIRT must be in open state to amend.")

    defect.project_code = kwargs['project_code']
    defect.release_id = kwargs['release_id']
    defect.priority = Priority.objects.get(id=kwargs['priority'])
    defect.reference = kwargs['reference']
    defect.description = kwargs['description']
    defect.comments = kwargs['comments']
    defect.save()
    
    data = {
        'project_code': defect.project_code,
        'release_id': defect.release_id,
        'priority': defect.priority.name,
        'reference': defect.reference,
        'description': defect.description,
        'comments': defect.comments
    }

    _save_event(DIRT_AMENDED, dirt_id, timezone.now(), kwargs['submitter'], data)

def reopen(dirt_id, user, release_id, reason):
    defect = Defect.objects.get(id=dirt_id)
    defect.reopen(release_id, reason)

    data = {
        'release_id': release_id,
        'reason': reason
    }
    
    _save_event(DIRT_REOPENED, dirt_id, timezone.now(), user, data)

def close_dirt(dirt_id, release_id, reason, user):
    defect = Defect.objects.get(id=dirt_id)
    defect.close(release_id)

    data = {
        'release_id': defect.release_id,
        'reason': reason
    }
    
    _save_event(DIRT_CLOSED, dirt_id, timezone.now(), user, data)

def delete_dirt(dirt_id, user):
    Defect.objects.get(id=dirt_id).delete()
    _save_event(DIRT_DELETED, dirt_id, timezone.now(), user, '{}')

def _save_event(event_type, dirt_id, date_occurred, username, dictionary):
    event = DomainEvent()
    event.event_type = event_type
    event.aggregate_id = dirt_id
    event.aggregate_type = 'DEFECT'
    event.date_occurred = date_occurred
    event.username = username
    event.blob = json.dumps(dictionary, indent=2)
    event.save()

def _close_dirt_desc(release_id, reason):
    if reason == '':
        return "DIRT closed. Version %s." % release_id
    return "DIRT closed. Version %s. [%s]" % (release_id, reason)