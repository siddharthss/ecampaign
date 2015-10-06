from django.conf.urls import url
from organization.views import OrganizationRegistrationView
from organization.views import DomainFormValidationView
# from organization.views import DomainFormView
from organization.views import ThankYouView

urlpatterns = [
    url(r'^registration/domain_form/(?P<pk>\d+)/$', DomainFormValidationView.as_view(), name='domain_view'),
    url(r'^registration/thankyou/(?P<domain_name>[\w-]+)/$', ThankYouView.as_view(), name='thank_you_view'),
    url(r'^registration', OrganizationRegistrationView.as_view(), name='org_reg_form'),
]


