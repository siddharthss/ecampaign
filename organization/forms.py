from collections import OrderedDict
from ckeditor.fields import RichTextField
import datetime
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm
from djcelery.models import PeriodicTask, CrontabSchedule
from .models import Organization, Lead, Campaign, Rule
from ckeditor.widgets import CKEditorWidget
from django.forms.extras.widgets import SelectDateWidget
from django_countries.widgets import CountrySelectWidget
from organization.tasks import send_onetime_mail, send_campaign
import json


class OrganizationRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    pin = forms.IntegerField()

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user:
                raise ValidationError(" duplicate email address.")
        except User.DoesNotExist:
            return email

    def clean(self):
        cleaned_data = super(OrganizationRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
                raise forms.ValidationError(
                    "Re enter the password.confirm password and password not matching. "
                )


class DomainForm(ModelForm):
    class Meta:
        model = Organization
        fields = ("domain_name",)

    def clean_domain_name(self):
        domain_name = self.cleaned_data['domain_name']

        if Organization.objects.filter(domain_name=domain_name).exists():
            raise ValidationError("this domain name already in use")
        else:
            return domain_name


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Remember Me', required=False)


class LeadForm(ModelForm):
    class Meta:
        model = Lead
        exclude = ["organization"]
        widgets = {'country': CountrySelectWidget()}


class CampaignForm(ModelForm):

    class Meta:
        model = Campaign
        exclude = ["organization","rule"]
        widgets = {
            'content': CKEditorWidget,
            'start_date': SelectDateWidget,
            'end_date': SelectDateWidget,
        }


class RuleForm(forms.Form):
    SOURCE_CHOICES = (('name', 'name'), ('address', 'address'), ('pin', 'pin'),
                      ('email', 'email'), ('country', 'country'))

    OPERATOR_CHOICES = (('icontains', 'icontains'), ('iexact', 'iexact'), ('lt', 'lt'),
                        ('lte', 'lte'), ('gt', 'gt'), ('gte', 'gte'))

    source = forms.ChoiceField(choices=SOURCE_CHOICES, required=True)
    operator = forms.ChoiceField(widget=forms.Select(), choices=OPERATOR_CHOICES, required=True)
    value = forms.CharField(max_length=100)


class CreateCampaignForm(forms.Form):
    SOURCE_CHOICES = (('name', 'name'), ('address', 'address'), ('pin', 'pin'),
                      ('email', 'email'), ('country', 'country'))

    OPERATOR_CHOICES = (('icontains', 'icontains'), ('iexact', 'iexact'), ('lt', 'lt'),
                        ('lte', 'lte'), ('gt', 'gt'), ('gte', 'gte'))

    SCHEDULE_TYPE_CHOICES = [('Onetime', 'Onetime'), ('Repetitive', 'Repetitive')]

    DAY_CHOICES = (('*', '*'), ('sunday', 'sunday'), ('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'),
                   ('thursday', 'thursday'), ('friday', 'friday'), ('saturday', 'saturday'))

    name = forms.CharField(max_length=100)
    start_date = forms.DateField()
    end_date = forms.DateField()
    subject = forms.CharField(max_length=100)
    content = forms.CharField(widget=CKEditorWidget())

    source = forms.ChoiceField(choices=SOURCE_CHOICES, required=True)
    operator = forms.ChoiceField(widget=forms.Select(), choices=OPERATOR_CHOICES, required=True)
    value = forms.CharField(max_length=100)

    schedule_type = forms.ChoiceField(widget=forms.Select(), choices=SCHEDULE_TYPE_CHOICES, initial='3', required=True,)
    schedule_date = forms.DateTimeField()
    schedule_time = forms.TimeField()
    minute = forms.CharField(max_length=10)
    hour = forms.CharField(max_length=10)

    day_of_week = forms.ChoiceField(widget=forms.Select(), choices=DAY_CHOICES, initial='3', required=True,)
    day_of_month = forms.CharField(max_length=10)
    month_of_year = forms.CharField(max_length=10)

    @transaction.atomic
    def save(self, user, commit=True):
        rule_data = dict(
            source=self.cleaned_data.pop('source'),
            value=self.cleaned_data.pop('value'),
            operator=self.cleaned_data.pop('operator')
        )
        rule = Rule.objects.create(**rule_data)

        schedule_data = dict(
            schedule_type=self.cleaned_data.pop('schedule_type'),
            schedule_date=self.cleaned_data.pop('schedule_date'),
            schedule_time=self.cleaned_data.pop('schedule_time')
        )
        campaign_data = dict(
            organization=Organization.objects.get(user=user),
            rule=rule,
            name=self.cleaned_data.pop('name'),
            start_date=self.cleaned_data.pop('start_date'),
            end_date=self.cleaned_data.pop('end_date'),
            subject=self.cleaned_data.pop('subject'),
            content=self.cleaned_data.pop('content'),
        )
        camp_obj = Campaign.objects.create(**campaign_data)
        self.run_campaign(schedule_data, camp_obj)

    def run_campaign(self, sdata, camp_object):
        if sdata['schedule_type'] == "Onetime":
            dt = datetime.datetime.combine(sdata['schedule_date'].date(), sdata['schedule_time'])
            send_onetime_mail.apply_async((camp_object.id,), eta=dt)
        elif sdata['schedule_type'] == "Repetitive":
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


class SendListLeadForm(forms.Form):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(SendListLeadForm, self).__init__(*args, **kwargs)
        self.fields = OrderedDict([('lead', forms.ModelMultipleChoiceField(
            queryset=Lead.objects.filter(organization=Organization.objects.get(user=request.user)),
            widget=forms.CheckboxSelectMultiple,
        )),])



