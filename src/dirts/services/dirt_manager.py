from dirts.models import Defect, Status

def latest_dirts():
    return Defect.objects.all().order_by('-date_created');

def get_detail(dirt_id):
    return Defect.objects.get(pk=dirt_id)

def raise_dirt(**kwargs):
    defect = Defect()
    _save(defect, **kwargs)

def amend_dirt(dirt_id, **kwargs):
    defect = Defect.objects.get(id=dirt_id)

    if defect.status.name != "Open":
        raise Exception("DIRT must be in open state to amend.")

    _save(defect, **kwargs)

def mark_accepted(dirt_id):
    pass

def mark_rejected(dirt_id, reason):
    pass

def close_dirt(dirt_id):
    pass

def _save(defect, **kwargs):
    defect.project_code = kwargs['project_code']
    defect.date_created = kwargs['date_created']
    defect.submitter = kwargs['submitter']
    defect.release_id = kwargs['release_id']
    defect.status = Status.objects.get(name='Open')
    defect.title = kwargs['title']
    defect.description = kwargs['description']
    defect.reference = kwargs['reference']
    defect.save()
