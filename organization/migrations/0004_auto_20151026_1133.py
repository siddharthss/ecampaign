# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20151026_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='country',
            field=models.CharField(default='abc', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='pin',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
    ]
