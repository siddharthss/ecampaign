# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20150930_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='domain_name',
            field=models.CharField(max_length=15, blank=True),
        ),
    ]
