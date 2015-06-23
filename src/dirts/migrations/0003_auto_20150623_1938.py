# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dirts', '0002_auto_20150622_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Severity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='defect',
            name='status',
            field=models.ForeignKey(to='dirts.Status', default=1),
        ),
        migrations.AddField(
            model_name='defect',
            name='severity',
            field=models.ForeignKey(to='dirts.Severity', default=1),
        ),
    ]
