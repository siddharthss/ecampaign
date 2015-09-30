# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_organization_domain_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='domain_name',
            field=models.CharField(unique=True, max_length=15, blank=True),
        ),
    ]
