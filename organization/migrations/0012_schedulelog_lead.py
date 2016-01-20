# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0011_auto_20160115_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulelog',
            name='lead',
            field=models.ForeignKey(default=1, to='organization.Lead'),
            preserve_default=False,
        ),
    ]
