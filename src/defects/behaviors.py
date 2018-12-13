import os

from django.utils import timezone
from haystack.query import SearchQuerySet

from common import store as EventStore

from .constants import DEFECT_OPENED
from .domain.models import DefectViewModel


class SimilarContentAware:
    def more_like_this(self, count = 5):
        if os.environ.get("DJANGO_SETTINGS_MODULE") != "config.prod":
            return []
        try:
            sqs = SearchQuerySet().more_like_this(self)[:count]
            return map(lambda x: x.object, sqs)
        except:
            return []

# eventually replace with user stories
class EventSourceAware:
    def as_domainmodel(self, before_date = None):
        events = EventStore.get_events_for('DEFECT', self.id, before_date)
        return DefectViewModel(events)