# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'f2ddec5e-822d-48a9-a766-7bde84c45036', unique=True, max_length=100)),
                ('local_file_path', models.CharField(default=b'5a660535-51f2-4f52-a482-3577f5ece47a', max_length=100)),
                ('hdfs_name', models.CharField(default=b'', unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'e8c4d728-1b18-4285-b99f-3730e90da0fc', unique=True, max_length=100)),
                ('status', models.CharField(default=b'created', max_length=100)),
                ('file', models.ForeignKey(to='webservice.File')),
            ],
        ),
    ]
