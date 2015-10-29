# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_lead'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='Lead_name',
            new_name='lead_name',
        ),
    ]
