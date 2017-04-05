# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0018_auto_20160212_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='rule',
        ),
        migrations.AddField(
            model_name='rule',
            name='campaign',
            field=models.ForeignKey(default=24, to='organization.Campaign'),
            preserve_default=False,
        ),
    ]
