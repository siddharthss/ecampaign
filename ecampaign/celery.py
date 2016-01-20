from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecampaign.settings')

app = Celery('ecampaign',
            include=['organization.tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERY_ENABLE_UTC=False,
    CELERY_TIMEZONE='Asia/Kolkata',
)


