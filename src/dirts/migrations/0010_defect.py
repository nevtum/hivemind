# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from dirts.models import Defect

def update_last_changed_dates(apps, schema_editor):
    defects = Defect.objects.all()
    for defect in defects:
        defect.date_changed = defect.date_created
        defect.save()
    
class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0009_auto_20160223_1737'),
    ]

    operations = [
        migrations.RunPython(update_last_changed_dates),
    ]
