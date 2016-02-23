# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0016_auto_20160209_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='filter',
        ),
        migrations.AddField(
            model_name='campaign',
            name='rule',
            field=models.ForeignKey(default=1, to='organization.Rule'),
            preserve_default=False,
        ),
    ]
