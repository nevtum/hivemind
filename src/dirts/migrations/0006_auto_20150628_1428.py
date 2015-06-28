# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0005_defecthistoryitem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Severity',
            new_name='Priority',
        ),
        migrations.RenameField(
            model_name='defect',
            old_name='severity',
            new_name='priority',
        ),
        migrations.RemoveField(
            model_name='defect',
            name='title',
        ),
        migrations.AddField(
            model_name='defect',
            name='comments',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='defect',
            name='reference',
            field=models.CharField(max_length=80),
        ),
    ]
