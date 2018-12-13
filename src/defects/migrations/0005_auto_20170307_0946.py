# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0004_fixtures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defect',
            name='date_changed',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='defect',
            name='date_created',
            field=models.DateTimeField(),
        ),
    ]
