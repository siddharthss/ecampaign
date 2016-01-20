# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('send_at', models.DateTimeField()),
                ('campaign', models.ForeignKey(to='organization.Campaign')),
            ],
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='campaign',
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]
