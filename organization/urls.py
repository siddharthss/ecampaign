from django.conf.urls import url
from organization.views import OrganizationRegistrationView, CreateLeadView, CreateCampaignView, ListLeadView, \
    ListCampaignView, SendCampaignListView, SendListLeadView, SendCampaignView, ScheduleLogView
from organization.views import DomainFormValidationView
from organization.views import ThankYouView
from organization.views import LogoutView

urlpatterns = [
    url(r'^registration/domain_form/(?P<pk>\d+)/$', DomainFormValidationView.as_view(), name='domain_view'),
    url(r'^registration/thankyou/(?P<domain_name>[\w-]+)/$', ThankYouView.as_view(), name='thank_you_view'),
    url(r'^registration/$', OrganizationRegistrationView.as_view(), name='org_reg_form'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^lead/$', CreateLeadView.as_view(), name='create_lead'),
    url(r'^campaign/$', CreateCampaignView.as_view(), name='create_campaign'),
    url(r'^list_lead/$', ListLeadView.as_view(), name='list_lead'),
    url(r'^list_campaign/$', ListCampaignView.as_view(), name='list_campaign'),
    url(r'^send_campaign/$', SendCampaignListView.as_view(), name='send_campaign'),
    url(r'^send_list_lead/(\d+)/$', SendListLeadView.as_view(), name='send_list_lead'),
    url(r'^send_list_lead/$', SendListLeadView.as_view(), name='send_list_lead'),
    url(r'^send/$', SendCampaignView.as_view(), name='send'),
    url(r'^schedule_log/$', ScheduleLogView.as_view(), name='schedule_log'),
]


