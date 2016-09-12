from common.models import DomainEvent
from dirts import constants
from dirts.models import Defect
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from feed.models import Activity
from django.utils import timezone


class Command(BaseCommand):
    help = """fix for updating last updated dates in DIRTs"""

    def handle(self, *args, **options):
        latest_datetime = self._get_datetime_last_activity()
        for event in DomainEvent.objects.filter(date_occurred__gt=latest_datetime):
            if event.event_type == constants.DIRT_OPENED:
                act = Activity()
                act.date_occurred = event.date_occurred
                act.summary = "A new DIRT has been created."
                act.submitter = get_object_or_404(User, username=event.username)
                act.project = get_object_or_404(Defect, id=event.aggregate_id).project
                act.content_type = ContentType.objects.get_for_model(Defect)
                act.object_id = event.aggregate_id
                act.save()
        
        self.stdout.write('updated feed')
    
    def _get_datetime_last_activity(self):
        last_activity = Activity.objects.last()

        if last_activity is None:
            return timezone.datetime(1970, 1, 1)

        return Activity.objects.last().date_occurred
