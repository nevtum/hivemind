# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.contrib.auth.models import User
from common.models import DomainEvent
from django.contrib.contenttypes.models import ContentType

def update_events(app, schema_editor):
    try:
        ct = ContentType.objects.get(model='defect')
        for event in DomainEvent.objects.all():
            event.owner = User.objects.get(username=event.username)
            event.object_id = event.aggregate_id
            if event.aggregate_type == 'DEFECT':
                event.content_type = ct
            event.save()
    except:
        print('Something went wrong in function -> update_events!')
        print('Please ignore if you are running tests!')

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('common', '0005_auto_20170309_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='domainevent',
            name='content_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domainevent',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domainevent',
            name='owner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RunPython(update_events)
    ]
