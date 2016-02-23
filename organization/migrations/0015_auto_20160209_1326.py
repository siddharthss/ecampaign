# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0014_auto_20160209_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='domain_name',
            field=models.CharField(unique=True, max_length=15, blank=True),
        ),
    ]
