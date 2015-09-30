from django.conf.urls import url
from organization.views import OrganizationRegistrationView
from organization.views import OrganizationRegistrationValidateView
from organization.views import DomainFormValidationView
from organization.views import DomainFormView


urlpatterns = [
    url(r'^registration/', OrganizationRegistrationView.as_view(), name='org_reg_form'),
    url(r'^reg_form/', OrganizationRegistrationValidateView.as_view(), name='org_reg_form_validate'),
    url(r'^domain_form/', DomainFormView.as_view(), name='domain_view'),
    url(r'^domain_validation_form/', DomainFormValidationView.as_view(), name='domain_validation_view'),
]


