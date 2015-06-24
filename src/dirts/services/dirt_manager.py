from django.db.models import Q
from dirts.models import Defect, Status, Severity

def latest_dirts(keyword):
    query = Q(title__contains=keyword) \
    | Q(description__contains=keyword) \
    | Q(reference__contains=keyword) \
    | Q(release_id__contains=keyword)

    return Defect.objects.filter(query).order_by('-date_created');

def get_detail(dirt_id):
    return Defect.objects.get(pk=dirt_id)

def raise_dirt(**kwargs):
    defect = Defect()
    defect.project_code = kwargs['project_code']
    defect.date_created = kwargs['date_created']
    defect.submitter = kwargs['submitter']
    defect.release_id = kwargs['release_id']
    defect.status = Status.objects.get(name='Open')
    defect.severity = Severity.objects.get(id=kwargs['severity_id'])
    defect.title = kwargs['title']
    defect.description = kwargs['description']
    defect.reference = kwargs['reference']
    defect.save()

def amend_dirt(dirt_id, **kwargs):
    defect = Defect.objects.get(id=dirt_id)

    if defect.status.name != "Open":
        raise Exception("DIRT must be in open state to amend.")

    defect.project_code = kwargs['project_code']
    defect.release_id = kwargs['release_id']
    defect.severity = Severity.objects.get(id=kwargs['severity_id'])
    defect.title = kwargs['title']
    defect.description = kwargs['description']
    defect.reference = kwargs['reference']
    defect.save()

def mark_accepted(dirt_id):
    pass

def mark_rejected(dirt_id, reason):
    pass

def close_dirt(dirt_id):
    pass
