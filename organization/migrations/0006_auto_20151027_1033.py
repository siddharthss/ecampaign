# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20151027_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='content',
            field=models.CharField(default='a', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaign',
            name='filter',
            field=models.CharField(default='as', max_length=100),
            preserve_default=False,
        ),
    ]
