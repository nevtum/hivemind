from .models import Defect
from common.models import Project, DomainEvent
from django.contrib.contenttypes.models import ContentType

def defect_activities(code):
    defect_ids = Defect.objects.filter(project_code__iexact=code).only('id').all()
    events = DomainEvent.objects.filter(
        content_type=ContentType.objects.get_for_model(Defect),
        object_id__in=defect_ids
    )
    events = events.select_related('owner', 'content_type')
    return events