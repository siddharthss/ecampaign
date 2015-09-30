# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20150929_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='domain_name',
            field=models.CharField(max_length=15, blank=True),
        ),
    ]
