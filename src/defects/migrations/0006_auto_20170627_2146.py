# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 11:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('defects', '0005_auto_20170307_0946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='defect',
            options={'ordering': ['-date_created']},
        ),
    ]