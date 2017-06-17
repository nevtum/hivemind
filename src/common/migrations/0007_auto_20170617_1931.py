# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20170617_1527'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='domainevent',
            unique_together=set([('content_type', 'object_id', 'sequence_nr')]),
        ),
        migrations.RemoveField(
            model_name='domainevent',
            name='aggregate_id',
        ),
        migrations.RemoveField(
            model_name='domainevent',
            name='aggregate_type',
        ),
        migrations.RemoveField(
            model_name='domainevent',
            name='username',
        ),
    ]
