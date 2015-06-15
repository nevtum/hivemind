# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20150503_0027'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendationSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Regulator',
            fields=[
                ('abbrev', models.CharField(serialize=False, primary_key=True, max_length=3, unique=True)),
                ('jurisdiction', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='recommendationsubscription',
            name='regulator',
            field=models.ForeignKey(to='clients.Regulator'),
        ),
        migrations.AddField(
            model_name='recommendationsubscription',
            name='user_id',
            field=models.ForeignKey(to='clients.Contact'),
        ),
    ]
