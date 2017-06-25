# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.contrib.auth.models import User
from common.models import DomainEvent

def update_events(app, schema_editor):
    try:
        for event in DomainEvent.objects.all():
            event.owner = User.objects.get(username=event.username)
            event.save()
    except Exception as e:
        print('Something went wrong in function -> update_events!')
        print(str(e))
        print('Please ignore if you are running tests!')
        # return # uncomment for testing
        raise Exception(e) # comment out for testing

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0005_auto_20170309_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='domainevent',
            name='owner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RunPython(update_events),
    ]
