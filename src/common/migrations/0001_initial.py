# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DomainEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=100)),
                ('aggregate_id', models.IntegerField()),
                ('blob', models.TextField()),
                ('date_occurred', models.DateTimeField()),
                ('username', models.CharField(max_length=50)),
            ],
        ),
    ]
