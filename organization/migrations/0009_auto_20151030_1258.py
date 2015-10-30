# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_auto_20151029_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='campaign_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='lead',
            name='lead_name',
            field=models.CharField(max_length=100),
        ),
    ]
