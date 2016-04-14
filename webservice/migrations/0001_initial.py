# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webservice.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(default=webservice.models.generate_uuid, unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=webservice.models.generate_uuid, unique=True, max_length=100)),
                ('status', models.CharField(default=b'created', max_length=100)),
                ('command', models.TextField(default=b'', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='execution',
            name='job',
            field=models.ForeignKey(to='webservice.Job'),
        ),
    ]
