# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defect',
            name='date_created',
            field=models.DateTimeField(),
        ),
    ]
