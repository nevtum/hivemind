import os

from django.utils import timezone
from haystack.query import SearchQuerySet

from common import store as EventStore

from .constants import DEFECT_OPENED
from .domain.models import DefectViewModel


class SimilarContentAware:
    def more_like_this(self, count = 5):
        if os.environ.get("DJANGO_SETTINGS_MODULE") != "config.settings.prod":
            return []
        try:
            sqs = SearchQuerySet().more_like_this(self)[:count]
            return map(lambda x: x.object, sqs)
        except:
            return []

class EventSourceAware:
    def as_domainmodel(self, before_date = None):
        events = EventStore.get_events_for('DEFECT', self.id, before_date)
        return DefectViewModel(events)
    
    def raise_new(self):
        self.save()
        event = {
            'sequence_nr': 0,
            'aggregate_id': self.id,
            'aggregate_type': 'DEFECT',
            'event_type': DEFECT_OPENED,
            'created': self.date_created,
            'created_by': self.submitter,
            'payload': {
                'project_code': self.project_code,
                'release_id': self.release_id,
                'priority': self.priority.name,
                'reference': self.reference,
                'description': self.description,
                'comments': self.comments
            }
        }
        EventStore.append_next(event)
        return event
    
    def amend(self, user):
        defect = self.as_domainmodel()
        event = defect.amend(user, timezone.now(), **self._to_kwargs())
        EventStore.append_next(event)
        self.save()
    
    def reopen(self, user, release_id, reason):
        defect = self.as_domainmodel()
        event = defect.reopen(user, release_id, reason, timezone.now())
        EventStore.append_next(event)

    def close(self, user, release_id, reason, timestamp=None):
        date_closed = timestamp if timestamp else timezone.now()
        if user is None:
            user = self.submitter.name
        if release_id is None:
            release_id = self.release_id
        defect = self.as_domainmodel()
        event = defect.close(user, release_id, reason, date_closed)
        EventStore.append_next(event)

    def _to_kwargs(self):
        return dict({
            'project_code': self.project_code,
            'submitter': self.submitter.username,
            'release_id': self.release_id,
            'status': self.status.name,
            'priority': self.priority.name,
            'reference': self.reference,
            'description': self.description,
            'comments': self.comments,
        })
