# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-11 06:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0006_auto_20150628_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defect',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]