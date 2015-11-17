from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
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
from .forms import OrganizationRegistrationForm, LeadForm, CampaignForm, SendListLeadForm
from .forms import DomainForm
from .forms import LoginForm
from .models import Organization, Lead, Campaign
from django.views.generic.edit import BaseFormView

class OrganizationRegistrationView(FormView):
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
        return super(CreateCampaignView, self).form_valid(form)

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
        organization = Organization.objects.get(user=self.request.user)
        queryset = Lead.objects.filter(organization=organization)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SendListLeadView, self).dispatch(*args, **kwargs)


class SendCampaignView(BaseFormView):
    def post(self, request):
        lead = request.POST.getlist('lead')
        queryset = Lead.objects.filter(pk__in=lead)
        messages.success(request, 'campaign is successfully send to leads')
        return redirect('send_list_lead')

    # form_class = SendListLeadForm
    #
    # def form_invalid(self, form):
    #     return HttpResponseRedirect(self.get_success_url())
    #
    # def form_valid(self, form):
    #     messages.success(self.request, 'campaign is successfully send to leads')
    #     return HttpResponseRedirect(self.get_success_url())
    #
    # def get_success_url(self):
    #     return reverse('send_list_lead')
    #
    #     # return reverse('dashboard_view')

