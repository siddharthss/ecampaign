# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0017_auto_20160210_1258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rule',
            old_name='name',
            new_name='source',
        ),
    ]
