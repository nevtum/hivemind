# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from dirts.models import Defect, Status, Priority
from common.models import DomainEvent

def load_fixtures(apps, schema_editor):
    Status.objects.get_or_create(name='Open')
    Status.objects.get_or_create(name='Closed')
    Priority.objects.get_or_create(name='High')
    Priority.objects.get_or_create(name='Medium')
    Priority.objects.get_or_create(name='Low')
    Priority.objects.get_or_create(name='Observational')

def update_last_changed_dates(apps, schema_editor):
    defects = Defect.objects.all()
    for defect in defects:
        events = DomainEvent.objects.filter(aggregate_type='DEFECT', aggregate_id=defect.id)
        if events:
            defect.date_changed = events.order_by('-date_occurred')[0].date_occurred
        else:
            defect.date_changed = defect.date_created
        
        defect.save()
    
class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0009_defecthistoryitem'),
    ]

    operations = [
        migrations.RunPython(update_last_changed_dates),
        migrations.RunPython(load_fixtures),
    ]
