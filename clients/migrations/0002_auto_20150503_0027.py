# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='role',
            field=models.ForeignKey(default=0, to='clients.WorkRole'),
            preserve_default=False,
        ),
    ]
