# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
        
class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_manufacturer_project'),
        ('dirts', '0002_fixtures'),
    ]

    operations = [
        migrations.AddField(
            model_name='defect',
            name='project',
            field=models.ForeignKey(to='common.Project', default=0),
            preserve_default=False,
        ),
    ]
