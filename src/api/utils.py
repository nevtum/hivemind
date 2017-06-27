from dirts.models import Defect
from common.models import Project, DomainEvent
from django.db.models import Q

def defect_activities(code, search_param):
    defects = Defect.objects.all()
    if code:
        defects = defects.filter(project_code__iexact=code)
    if search_param:
        defects = defects.filter(
            Q(reference__icontains=search_param) |
            Q(description__icontains=search_param) |
            Q(comments__icontains=search_param)
        )
    defect_ids = defects.only('id').all()

    events = DomainEvent.objects.filter(
        aggregate_type='DEFECT',
        aggregate_id__in=defect_ids
    )
    events = events.select_related('owner')
    return events