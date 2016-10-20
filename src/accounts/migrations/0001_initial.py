# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignupRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pending_approval', models.BooleanField(default=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('hashed_password', models.CharField(max_length=100)),
                ('iterations', models.IntegerField()),
                ('salt', models.CharField(max_length=50)),
            ],
        ),
    ]
