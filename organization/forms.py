from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput
from .models import Organization, Lead, Campaign
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.forms.extras.widgets import SelectDateWidget

class OrganizationRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    organization_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    pin = forms.IntegerField()
    # username = forms.CharField(widget=CKEditorWidget())


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
