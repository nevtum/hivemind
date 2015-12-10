import json
from django.utils import timezone
from django.db.models import Q
from common.models import DomainEvent

from dirts.models import Defect, Status, Priority, DefectHistoryItem

def latest_dirts(keyword):
    query = Q(reference__icontains=keyword) \
    | Q(project_code__icontains=keyword) \
    | Q(description__icontains=keyword) \
    | Q(comments__icontains=keyword) \
    | Q(release_id__icontains=keyword)

    return Defect.objects.filter(query).order_by('-date_created')

def get_detail(dirt_id):
    return Defect.objects.get(pk=dirt_id)

def get_history(dirt_id):
    return DefectHistoryItem.objects.filter(defect=dirt_id).order_by('-date_created')

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
    
    event = DomainEvent()
    event.event_type = 'DIRT.OPENED'
    event.aggregate_id = defect.id
    event.date_occurred = defect.date_created
    event.username = defect.submitter.username
    event.blob = json.dumps(data)
    event.save()

    entry = DefectHistoryItem()
    entry.date_created = kwargs['date_created']
    entry.defect = defect
    entry.short_desc = "DIRT created."
    entry.submitter = kwargs['submitter']
    entry.save()
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

    entry = DefectHistoryItem()
    entry.date_created = kwargs['date_created']
    entry.defect = defect
    entry.short_desc = "DIRT amended."
    entry.submitter = kwargs['submitter']
    entry.save()

def reopen(dirt_id, user, release_id, reason):
    defect = Defect.objects.get(id=dirt_id)
    defect.reopen(release_id, reason)

    entry = DefectHistoryItem()
    entry.date_created = timezone.now()
    entry.defect = defect
    entry.short_desc = "Reopened. Version %s. [%s]" % (release_id, reason)
    entry.submitter = user
    entry.save()

def mark_accepted(dirt_id):
    pass

def mark_rejected(dirt_id, reason):
    pass

def close_dirt(dirt_id, user):
    defect = Defect.objects.get(id=dirt_id)
    defect.close()

    entry = DefectHistoryItem()
    entry.date_created = timezone.now()
    entry.defect = defect
    entry.short_desc = "DIRT closed. Version %s." % defect.release_id
    entry.submitter = user
    entry.save()

def delete_dirt(dirt_id):
    Defect.objects.get(id=dirt_id).delete()
    DefectHistoryItem.objects.filter(defect=dirt_id).delete()
