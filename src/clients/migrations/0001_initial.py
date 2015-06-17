# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('employed_by', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=5, choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.')])),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Jurisdiction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=40)),
                ('abbrev', models.CharField(max_length=10)),
                ('regulator', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='RecommendationSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('jurisdiction', models.ForeignKey(to='clients.Jurisdiction')),
                ('user_id', models.ForeignKey(to='clients.Contact')),
            ],
        ),
    ]
