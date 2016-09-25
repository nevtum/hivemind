from common.models import DomainEvent
from dirts import constants
from dirts.models import Defect
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils import timezone
from feed.models import Activity


class Command(BaseCommand):
    help = """background running process which updates feed
    base on events that have occurred."""

    def handle(self, *args, **options):
        latest_datetime = self._get_datetime_last_activity()
        for event in DomainEvent.objects.filter(date_occurred__gt=latest_datetime):
            try:
                if event.event_type == constants.DIRT_OPENED:
                    self._handle_DIRT_OPENED(event)
                if event.event_type == constants.DIRT_CLOSED:
                    self._handle_DIRT_CLOSED(event)
                if event.event_type == constants.DIRT_REOPENED:
                    self._handle_DIRT_REOPENED(event)
            except Exception as e:
                print(e)
        
        self.stdout.write('updated feed')

    def _handle_DIRT_OPENED(self, event):
        act = self._to_activity(event)
        act.summary = "A new DIRT has been created."
        act.save()
    
    def _handle_DIRT_CLOSED(self, event):
        act = self._to_activity(event)
        act.summary = "A DIRT has been closed."
        act.save()

    def _handle_DIRT_REOPENED(self, event):
        act = self._to_activity(event)
        act.summary = "An existing DIRT has been reopened."
        act.save()
    
    def _to_activity(self, event):
        act = Activity()
        print(event.date_occurred)
        act.date_occurred = event.date_occurred
        act.submitter = get_object_or_404(User, username=event.username)
        act.project = get_object_or_404(Defect, id=event.aggregate_id).project
        act.content_type = ContentType.objects.get_for_model(Defect)
        act.object_id = event.aggregate_id
        return act
    
    def _get_datetime_last_activity(self):
        last_activity = Activity.objects.last()

        if last_activity is None:
            return timezone.datetime(1970, 1, 1)

        return Activity.objects.last().date_occurred
