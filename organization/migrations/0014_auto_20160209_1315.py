# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0013_auto_20160209_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
