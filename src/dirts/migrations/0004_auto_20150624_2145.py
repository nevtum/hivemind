# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0003_auto_20150623_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defect',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='defect',
            name='reference',
            field=models.TextField(default='N/A'),
        ),
    ]
