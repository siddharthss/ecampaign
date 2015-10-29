# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_campaign_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='subject',
            field=models.CharField(max_length=100),
        ),
    ]
