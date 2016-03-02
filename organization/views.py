from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
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
from .forms import OrganizationRegistrationForm, LeadForm, SendListLeadForm, CreateCampaignForm
from .forms import DomainForm
from .forms import LoginForm
from organization.models import Organization, Lead, Campaign, ScheduleLog, Rule
from organization.tasks import send_campaign


class OrganizationRegistrationView(FormView):
    """for organization reg."""
    template_name = "organization/organization_registration.html"
    form_class = OrganizationRegistrationForm

    def form_valid(self, form):
        first_name = form.cleaned_data.pop('first_name')
        last_name = form.cleaned_data.pop('last_name')
        email = form.cleaned_data.pop('email')
        password = form.cleaned_data.pop('password')
        name = form.cleaned_data.pop('name')
        address = form.cleaned_data.pop('address')
        pin = form.cleaned_data.pop('pin')

        user_object = User.objects.create_user(username=email, email=email, password=password,
                                               first_name=first_name, last_name=last_name,)
        organization_object = Organization.objects.create(
            name=name, address=address,
            pin=pin, user=user_object
        )
        self.object = organization_object
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
        username = form.cleaned_data.pop('username')
        password = form.cleaned_data.pop('password')
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


class CreateCampaignView(FormView):
    template_name = 'organization/create_campaign.html'
    form_class = CreateCampaignForm

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        import ipdb;ipdb.set_trace()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        import ipdb;ipdb.set_trace()

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
        org = Organization.objects.get(user=self.request.user)
        queryset = Lead.objects.filter(organization=org)      
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(SendListLeadView, self).get_context_data(**kwargs)
        context['campaign_id'] = self.args[0]
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SendListLeadView, self).dispatch(*args, **kwargs)


class SendCampaignView(View):

    def post(self, request):
        campaign_id = request.POST['campaign_id']
        form = SendListLeadForm(request.POST, request=request)
        if form.is_valid():
            lead = request.POST.getlist('lead')
            queryset = Lead.objects.filter(pk__in=lead)
            campaign_object = Campaign.objects.get(id=campaign_id)
            send_campaign.apply_async((queryset, campaign_object))
            messages.success(request, 'campaign is successfully send to leads')
        else:
            messages.error(request, 'Please select leads ')
        return redirect('send_list_lead', campaign_id)


class ScheduleLogView(ListView):
    model = ScheduleLog
    template_name = 'organization/schedule_log.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ScheduleLogView, self).get_context_data(**kwargs)
        schedule_log_list = ScheduleLog.objects.all()
        paginator = Paginator(schedule_log_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            file_schedule_log = paginator.page(page)
        except PageNotAnInteger:
            file_schedule_log = paginator.page(1)
        except EmptyPage:
            file_schedule_log = paginator.page(paginator.num_pages)
        context['schedule_log_list'] = file_schedule_log
        return context


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ScheduleLogView, self).dispatch(*args, **kwargs)
