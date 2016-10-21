# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signuprequest',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='signuprequest',
            name='first_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signuprequest',
            name='last_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
