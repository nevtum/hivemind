# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-23 06:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20151213_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainevent',
            name='date_occurred',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]