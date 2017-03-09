# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_manufacturer_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainevent',
            name='date_occurred',
            field=models.DateTimeField(),
        ),
    ]
