# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization_name', models.CharField(unique=True, max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('pin', models.IntegerField()),
                ('domain_name', models.CharField(max_length=15, blank=True)),
                ('user_fk', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
