# an emergency script to build Defect objects out of domain events 

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from common.models import DomainEvent, Project
from common import store as Eventstore
from dirts.domain.models import DefectViewModel
from dirts.models import Defect, Status, Priority

class Command(BaseCommand):
    help = """rebuild all DIRT aggregates using sequence of events 
    stored in the database"""

    def handle(self, *args, **options):
        for id in self.unique_ids():
            events = Eventstore.get_events_for('DEFECT', id)
            defect = self.build_defect_read_model(events)
            defect.save()

    def unique_ids(self):
        defect_events = DomainEvent.objects.filter(aggregate_type='DEFECT')
        ids = defect_events.values_list('aggregate_id', flat=True)
        return ids.distinct()
            
    def build_defect_read_model(self, events):
        aggregate = DefectViewModel(events)
        d = Defect(id=aggregate.id)
        d.project_code = aggregate.project_code
        d.project = Project.objects.get(code=aggregate.project_code)
        d.date_created = aggregate.date_created
        d.date_changed = aggregate.date_changed
        d.submitter = User.objects.get(username=aggregate.submitter)
        d.release_id = aggregate.release_id
        d.status = Status.objects.get(name=aggregate.status)
        d.priority = Priority.objects.get(name=aggregate.priority)
        d.reference = aggregate.reference
        d.description = aggregate.description
        d.comments = aggregate.comments
        return d