# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from common.models import DomainEvent
from dirts.constants import DIRT_OPENED, DIRT_CLOSED
from dirts.models import Defect, DefectHistoryItem
import json

def migrate_to_events(apps, schema_editor):
    defects = Defect.objects.all()
    for d in defects:
        data = {
            'project_code': d.project_code,
            'release_id': d.release_id,
            'priority': d.priority.name,
            'reference': d.reference,
            'description': d.description,
            'comments': d.comments
        }
        
        openevent = DomainEvent()
        openevent.event_type = DIRT_OPENED
        openevent.aggregate_id = int(d.id)
        openevent.aggregate_type = 'DEFECT'
        openevent.date_occurred = d.date_created
        openevent.username = d.submitter.username
        openevent.blob = json.dumps(data, indent=2)
        openevent.save()
        
        closedata = {
            'release_id': d.release_id,
            'reason': ""
        }
        
        closeevent = DomainEvent()
        closeevent.event_type = DIRT_CLOSED
        closeevent.aggregate_id = int(d.id)
        closeevent.aggregate_type = 'DEFECT'
        closeevent.date_occurred = d.date_created
        closeevent.username = d.submitter.username
        closeevent.blob = json.dumps(closedata, indent=2)
        closeevent.save()
    
class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0007_auto_20151211_1730'),
    ]

    operations = [
        migrations.RunPython(migrate_to_events),
    ]
