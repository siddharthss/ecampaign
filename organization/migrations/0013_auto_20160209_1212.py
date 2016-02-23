# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0012_schedulelog_lead'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('operator', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='campaign',
            old_name='campaign_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='lead',
            old_name='lead_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='organization_name',
            new_name='name',
        ),
    ]
