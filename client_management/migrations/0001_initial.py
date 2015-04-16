# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('name', models.CharField(max_length=40)),
                ('code', models.CharField(max_length=20, unique=True, serialize=False, primary_key=True)),
                ('status', models.CharField(default='OP', choices=[('OP', 'Operational'), ('NOOP', 'Non-Operational')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.')], max_length=5)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('company', models.ForeignKey(to='client_management.Company')),
            ],
        ),
    ]
