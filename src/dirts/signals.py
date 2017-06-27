from django.db.models.signals import post_save

from common import store as EventStore

from .constants import DEFECT_OPENED
from .models import Defect


def on_defect_created(sender, instance, **kwargs):
    if not kwargs['created']:
        return
    
    event = {
        'timestamp': instance.date_created,
        'sequence_nr': 0,
        'aggregate_id': instance.id,
        'aggregate_type': 'DEFECT',
        'event_type': DEFECT_OPENED,
        'payload': {
            'project_code': instance.project_code,
            'release_id': instance.release_id,
            'priority': instance.priority.name,
            'reference': instance.reference,
            'description': instance.description,
            'comments': instance.comments
        },
        'owner': {
            'username': instance.submitter.username,
            'email': instance.submitter.email
        }
    }
    EventStore.append_next(event)

post_save.connect(on_defect_created, sender=Defect)
