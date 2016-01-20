from __future__ import absolute_import
import datetime
from django.core.mail import EmailMessage

from ecampaign.celery import app
from organization.models import Lead, Organization, ScheduleLog, Campaign


@app.task()
def send_onetime_mail(campaign_object, org):
    queryset = Lead.objects.filter(organization=org)
    for obj in queryset:
        msg = EmailMessage(campaign_object.subject, campaign_object.content, 'noreply@vertisinfotech.com', [obj.email])
        msg.content_subtype = "html"
        msg.send()
        time = datetime.datetime.now()
        log = ScheduleLog.objects.create(campaign=campaign_object, lead=obj, send_at=time)
        log.save()
    return 1


@app.task()
def send_repetitive_mail(name, subject, content, org):
    org = Organization.objects.get(pk=org)
    queryset = Lead.objects.filter(organization=org)
    campaign = Campaign.objects.get(name=name)
    send_at = datetime.datetime.now()
    ScheduleLog.objects.create(campaign=campaign, sent_at=send_at)
    for obj in queryset:
        msg = EmailMessage(subject, content, 'noreply@vertisinfotech.com', [obj.email])
        msg.content_subtype = "html"
        msg.send()
        time = datetime.datetime.now()
        log = ScheduleLog.objects.create(campaign=campaign, lead=obj, send_at=time)
        log.save()
    return 1
