# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from dirts.models import Status, Priority

def load_fixtures(apps, schema_editor):
    Status.objects.get_or_create(name='Open')
    Status.objects.get_or_create(name='Closed')
    Priority.objects.get_or_create(name='High')
    Priority.objects.get_or_create(name='Medium')
    Priority.objects.get_or_create(name='Low')
    Priority.objects.get_or_create(name='Observational')
    
class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixtures),
    ]
