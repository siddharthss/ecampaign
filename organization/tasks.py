import datetime
from django.core.mail import EmailMessage
from django.db.models import Q
import operator
from ecampaign.celery import app
from organization.models import Lead, Organization, ScheduleLog, Campaign, Rule


@app.task()
def send_campaign(queryset, campaign_object):
    content = campaign_object.content
    for obj in queryset:
        msg = EmailMessage('Test mail', content, 'noreply@vertisinfotech.com', [obj.email])
        msg.content_subtype = "html"
        msg.send()
        time = datetime.datetime.now()
        ScheduleLog.objects.create(campaign=campaign_object, lead=obj, send_at=time)

@app.task()
def send_onetime_mail(campaign_object_id):
    campaign_object = Campaign.objects.get(id=campaign_object_id)
    rules = Rule.objects.filter(campaign=campaign_object)
    predicates = []
    for rule in rules:
        if predicates == 0:
            predicates = [(rule.source+'__'+rule.operator, rule.value), ]
        else:
            predicates.append((rule.source+'__'+rule.operator, rule.value),)
    q_list = [Q(x) for x in predicates]
    queryset = Lead.objects.filter(reduce(operator.or_, q_list))
    for obj in queryset:
        msg = EmailMessage(campaign_object.subject, campaign_object.content, 'noreply@vertisinfotech.com', [obj.email])
        msg.content_subtype = "html"
        msg.send()
        current_time = datetime.datetime.now()
        ScheduleLog.objects.create(campaign=campaign_object, lead=obj, send_at=current_time)

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
        current_time = datetime.datetime.now()
        ScheduleLog.objects.create(campaign=campaign, lead=obj, send_at=current_time)


@app.task()
def demo_task():
    obj = Lead.objects.filter(name='deepak')[0]
    obj.pin += 1
    obj.save()

