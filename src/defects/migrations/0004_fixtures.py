# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone
from common.models import Project, Manufacturer
from defects.models import Defect

def load_fixtures(apps, schema_editor):
    for defect in Defect.objects.all():
        create_project_from(defect)

def create_project_from(defect):
    manufacturer = create_manufacturer_from(defect.project_code)
    project, created = Project.objects.get_or_create(
        code=defect.project_code,
        manufacturer=manufacturer,
        date_created=timezone.now()
    )
    defect.project = project
    defect.save()
    
def create_manufacturer_from(code):
    if 'AGT' in code.upper():
        m, c = Manufacturer.objects.get_or_create(
            name="Ainsworth",
            is_operational=True
        )
        return m
    if 'STG' in code.upper():
        m, c = Manufacturer.objects.get_or_create(
            name="Bally",
            is_operational=True
        )
        return m
    else:
        m, c = Manufacturer.objects.get_or_create(
            name="N/A",
            is_operational=False
        )
        return m
        
class Migration(migrations.Migration):

    dependencies = [
        ('defects', '0003_defect_project'),
    ]

    operations = [
        migrations.RunPython(load_fixtures),
    ]
