from datetime import timedelta, datetime
import json
import uuid
from celery.schedules import crontab_parser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib import messages
from djcelery.schedulers import ModelEntry
from .forms import OrganizationRegistrationForm, LeadForm, CampaignForm, SendListLeadForm
from .forms import DomainForm
from .forms import LoginForm
import organization
from organization.models import Organization, Lead, Campaign, ScheduleLog
from organization.tasks import send_onetime_mail

import dateutil.parser
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule


class OrganizationRegistrationView(FormView):
    """for organization reg."""
    template_name = "organization/organization_registration.html"
    form_class = OrganizationRegistrationForm

    def form_valid(self, form):
        first_name = self.request.POST['first_name']
        last_name = self.request.POST['last_name']
        email = self.request.POST['email']
        password = self.request.POST['password']
        organization_name = self.request.POST['organization_name']
        address = self.request.POST['address']
        pin = self.request.POST['pin']
        user_object = User.objects.create_user(username=email, email=email, password=password,
                                               first_name=first_name, last_name=last_name,)
        user_object.save()
        organization_object = Organization.objects.create(
            organization_name=organization_name, address=address,
            pin=pin, user=user_object
        )
        self.object = organization_object
        organization_object.save()
        return super(OrganizationRegistrationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('domain_view', kwargs={'pk': self.object.id})


class DomainFormValidationView(UpdateView):
    form_class = DomainForm
    model = Organization
    template_name = 'organization/domain_form.html'

    def get_success_url(self):
        return reverse('thank_you_view', kwargs={'domain_name': self.object.domain_name})


class ThankYouView(TemplateView):
    """to render the domain_form"""
    template_name = 'organization/thankyou.html'


class LoginView(FormView):
    """"""
    form_class = LoginForm
    template_name = "organization/organization_login.html"

    def form_valid(self, form):
        host = self.request.META['HTTP_HOST']
        arr = host.split(".")
        host = arr[0]
        obj = get_object_or_404(Organization, domain_name=host)
        username = self.request.POST['username']
        password = self.request.POST['password'] 
        user = authenticate(username=username, password=password)

        if user == obj.user:
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    remember_me = self.request.POST.get('remember_me')
                    if remember_me == "on":
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                    else:
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                    return super(LoginView, self).form_valid(form)
                else:
                    return self.form_invalid(form)
            else:
                messages.error(self.request, "invalid email or password")
                return self.form_invalid(form)
        else:
            messages.error(self.request, "invalid email or password")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('dashboard_view')


class DashboardView(TemplateView):
    """to render the domain_form"""
    template_name = 'organization/dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login_view')


class DemoView(View):
    """to render the domain_form"""
    template_name = 'organization/demo.html'

    def get(self, request, *args, **kwargs):
        host = request.META['HTTP_HOST']
        arr = host.split(".")
        host = arr[0]
        return render(request, self.template_name, {'hostname': host})


class CreateLeadView(CreateView):
    model = Lead
    template_name = 'organization/create_lead.html'
    form_class = LeadForm

    def form_valid(self, form):
        form.instance.organization = Organization.objects.get(user=self.request.user)
        return super(CreateLeadView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard_view')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateLeadView, self).dispatch(*args, **kwargs)


class CreateCampaignView(CreateView):
    model = Campaign
    template_name = 'organization/create_campaign.html'
    form_class = CampaignForm

    def form_valid(self, form):
        form.instance.organization = Organization.objects.get(user=self.request.user)
        schedule_type = self.request.POST["schedule_type"]
        schedule_date = self.request.POST["schedule_date"]
        schedule_time = self.request.POST["schedule_time"]

        cron_minute = crontab_parser(60).parse(self.request.POST["minute"])
        cron_hour = crontab_parser(24).parse(self.request.POST["hour"])
        day_of_week = crontab_parser(7).parse(self.request.POST["day_of_week"])
        day_of_month = crontab_parser(31, 1).parse(self.request.POST["day_of_month"])
        month_of_year = crontab_parser(12, 1).parse(self.request.POST["month_of_year"])

        expire_date = self.request.POST["end_date"]
        name = self.request.POST['campaign_name']
        subject = self.request.POST['subject']
        content = self.request.POST['content']
        filter = self.request.POST['filter']
        org = form.instance.organization
        orgpk = form.instance.organization.pk

        self.object = form.save()

        if schedule_type == "Onetime":
            dt = schedule_date+schedule_time+':00'
            date_iso = datetime.strptime(dt, '%Y-%m-%d%H:%M:%S')
            date_iso = date_iso.isoformat()
            date_object = datetime.strptime(date_iso, '%Y-%m-%dT%H:%M:%S')
            send_onetime_mail.apply_async((self.object, org), eta=date_object)
        elif schedule_type == "Repetitive":
            cron = CrontabSchedule.objects.create()
            pargs = json.dumps(["Test Mail 3", "Throgh app"])
            periodic_task = PeriodicTask.objects.create(name="Run Campaign",
                                                        task="organization.tasks.send_repetitive_mail",
                                                        crontab=cron, args=pargs)
            # cron = CrontabSchedule.objects.create(minute=cron_minute, hour=cron_hour,day_of_week=day_of_week,
            #                                       day_of_month=day_of_month, month_of_year=month_of_year,)
            #
            # pargs = json.dumps([name, subject, content,  orgpk])
            # periodic_task = PeriodicTask.objects.create(name=uuid.uuid4(),
            #                                             task="organization.tasks.send_repetitive_mail",
            #                                             crontab=cron, args=pargs)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('dashboard_view')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateCampaignView, self).dispatch(*args, **kwargs)


class ListLeadView(ListView):
    model = Lead
    template_name = 'organization/list_lead.html'

    def get_queryset(self):
        organization = Organization.objects.get(user=self.request.user)
        queryset = Lead.objects.filter(organization=organization)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListLeadView, self).dispatch(*args, **kwargs)


class ListCampaignView(ListView):
    model = Campaign
    template_name = 'organization/list_campaign.html'

    def get_queryset(self):
        organization = Organization.objects.get(user=self.request.user)
        queryset = Campaign.objects.filter(organization=organization)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListCampaignView, self).dispatch(*args, **kwargs)


class SendCampaignListView(ListView):
    model = Campaign
    template_name = 'organization/send_campaign.html'

    def get_queryset(self):
        organization = Organization.objects.get(user=self.request.user)
        queryset = Campaign.objects.filter(organization=organization)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SendCampaignListView, self).dispatch(*args, **kwargs)


class SendListLeadView(ListView):
    model = Lead
    template_name = 'organization/send_list_lead.html'

    def get_queryset(self):
        # cron = CrontabSchedule.objects.create()
        # pargs = json.dumps(["Test Mail 3", "Through app"])
        # periodic_task = PeriodicTask.objects.create(name="Run Campaign",
        #                                             task="organization.tasks.send_repetitive_mail",
        #                                             crontab=cron, args=pargs)
        #
        org=Organization.objects.get(user=self.request.user)
        queryset = Lead.objects.filter(organization=org)      
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(SendListLeadView, self).get_context_data(**kwargs)
        context['campaign_id'] = self.args[0]
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SendListLeadView, self).dispatch(*args, **kwargs)


class SendCampaignView(View):

    def post(self, request):
        campaign_id = request.POST['campaign_id']
        form = SendListLeadForm(request.POST, request=request)
        if form.is_valid():
            lead = request.POST.getlist('lead')
            queryset = Lead.objects.filter(pk__in=lead)
            campaign_object = Campaign.objects.get(id=campaign_id)
            content = campaign_object.content
            for obj in queryset:
                msg = EmailMessage('Test mail', content, 'noreply@vertisinfotech.com', [obj.email])
                msg.content_subtype = "html"
                msg.send()
                time = datetime.now()
                log = ScheduleLog.objects.create(campaign=campaign_object, lead=obj, send_at=time)
                log.save()
            messages.success(request, 'campaign is successfully send to leads')
        else:
            messages.error(request, 'Please select leads ')
        return redirect('send_list_lead', campaign_id)


class ScheduleLogView(ListView):
    model = ScheduleLog
    template_name = 'organization/schedule_log.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScheduleLogView, self).dispatch(*args, **kwargs)
