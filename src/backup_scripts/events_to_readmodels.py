# an emergency script to build Defect objects out of domain events 

import os, sys
from django.core.wsgi import get_wsgi_application

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "echelon.settings.prod")
application = get_wsgi_application()

from django.contrib.auth.models import User
from common.models import DomainEvent, Project
from common import store as Eventstore
from dirts.domain.models import DefectViewModel
from dirts.models import Defect, Status, Priority

def main():
    for id in unique_ids():
        events = Eventstore.get_events_for('DEFECT', id)
        defect = build_defect_read_model(events)
        defect.save()

def unique_ids():
    defect_events = DomainEvent.objects.filter(aggregate_type='DEFECT')
    ids = defect_events.values_list('aggregate_id', flat=True)
    return ids.distinct()
        
def build_defect_read_model(events):
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

if __name__ == '__main__':
    main()