from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Organization


class OrganizationRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    organization_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    pin = forms.IntegerField()

    # class Meta:
    #     model = Organization
    #     exclude = ["domain_name","user_fk"]
    #     widgets = {
    #     'password': forms.PasswordInput(),
    #     'phone': forms.NumberInput(),
    #     }


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




