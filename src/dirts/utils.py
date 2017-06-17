from .models import Defect
from common.models import Project, DomainEvent

def defect_activities(code):
    defect_ids = Defect.objects.filter(project_code__iexact=code).only('id').all()
    events = DomainEvent.objects.filter(
        aggregate_type='DEFECT',
        aggregate_id__in=defect_ids
    )
    events = events.order_by('aggregate_id', 'sequence_nr')
    return events