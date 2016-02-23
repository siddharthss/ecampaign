# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0015_auto_20160209_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
