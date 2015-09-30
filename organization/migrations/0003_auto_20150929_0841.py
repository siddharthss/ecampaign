# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20150928_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organization_name',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
