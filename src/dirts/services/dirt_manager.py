from dirts.models import Defect

def raise_dirt(**kwargs):
    defect = Defect()
    defect.project_code = kwargs['project_code']
    defect.date_created = kwargs['date_created']
    defect.submitter = kwargs['submitter']
    defect.release_id = kwargs['release_id']
    defect.title = kwargs['title']
    defect.description = kwargs['description']
    defect.reference = kwargs['reference']
    defect.save()

def amend_dirt(dirt_id, **kwargs):
    pass

def mark_accepted(dirt_id):
    pass

def mark_rejected(dirt_id, reason):
    pass

def close_dirt(dirt_id):
    pass
