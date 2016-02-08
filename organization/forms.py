from collections import OrderedDict
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Organization, Lead, Campaign
from ckeditor.widgets import CKEditorWidget
from django.forms.extras.widgets import SelectDateWidget


class OrganizationRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    organization_name = forms.CharField(max_length=100)
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


class CampaignForm(ModelForm):

    class Meta:
        model = Campaign
        exclude = ["organization"]
        widgets = {
            'content': CKEditorWidget,
            'start_date': SelectDateWidget,
            'end_date': SelectDateWidget,
        }


class SendListLeadForm(forms.Form):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(SendListLeadForm, self).__init__(*args, **kwargs)
        self.fields = OrderedDict([('lead', forms.ModelMultipleChoiceField(
            queryset=Lead.objects.filter(organization=Organization.objects.get(user=request.user)),
            widget=forms.CheckboxSelectMultiple,
        )),])


# class ScheduleForm(ModelForm):
#     class Meta:
#         model = Schedule
#         exclude = [""]

