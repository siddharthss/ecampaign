# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20151027_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='subject',
            field=ckeditor.fields.RichTextField(default='abc'),
            preserve_default=False,
        ),
    ]
