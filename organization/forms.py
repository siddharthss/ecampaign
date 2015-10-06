from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Organization


class OrganizationRegistrationForm(ModelForm):
    class Meta:
        model = Organization
        exclude = ["domain_name"]
        widgets = {
        'password': forms.PasswordInput(),
        'phone': forms.NumberInput(),
        }


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
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean(self):
    #     host = self.request.META['HTTP_HOST']
    #     arr = host.split(".")
    #     host = arr[0]
    #     obj = Organization.objects.filter(domain_name=host)
    #
    #     if obj.exists():
    #         if obj.get().email != (self.cleaned_data.get('email') or obj.get().password != self.cleaned_data.get('password')):
    #             raise ValidationError("invalid Email addresses Or password.")
    #     else:
    #         raise ValidationError("invalid Email addresses Or password.")
    #
    #     return self.cleaned_data



