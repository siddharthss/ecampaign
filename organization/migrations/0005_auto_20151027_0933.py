# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20151026_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign_name', models.CharField(unique=True, max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.RenameField(
            model_name='lead',
            old_name='organization_fk',
            new_name='organization',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='user_fk',
            new_name='user',
        ),
        migrations.AddField(
            model_name='campaign',
            name='organization',
            field=models.ForeignKey(to='organization.Organization'),
        ),
    ]
