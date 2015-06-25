# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dirts', '0004_auto_20150624_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefectHistoryItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField()),
                ('short_desc', models.CharField(max_length=80)),
                ('defect', models.ForeignKey(to='dirts.Defect')),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
