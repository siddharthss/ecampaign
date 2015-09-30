from django import forms
from django.forms import ModelForm
from .models import Organization
from .models import Organization


class OrganizationRegistrationForm(ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        widgets = {
        'password': forms.PasswordInput(),
        'phone': forms.NumberInput(),
        }


class DomainForm(forms.Form):
    domain_name = forms.CharField(max_length= 20)
    pk = forms.IntegerField()
