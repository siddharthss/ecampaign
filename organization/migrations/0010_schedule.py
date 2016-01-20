# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_auto_20151030_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=15)),
                ('date', models.DateField()),
                ('day', models.CharField(max_length=15)),
                ('time', models.TimeField()),
                ('campaign', models.ForeignKey(to='organization.Campaign')),
            ],
        ),
    ]
