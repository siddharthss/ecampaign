from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from .forms import OrganizationRegistrationForm
from .forms import DomainForm
from .forms import LoginForm
from .models import Organization
# Create your views here.


class OrganizationRegistrationView(CreateView):
    model = Organization
    template_name = "organization/organization_registration.html"
    form_class = OrganizationRegistrationForm

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
    form_class = LoginForm
    template_name = "organization/organization_login.html"

    def form_valid(self, form):
        host = self.request.META['HTTP_HOST']
        arr = host.split(".")
        host = arr[0]
        obj = Organization.objects.filter(domain_name=host)

        if obj.exists():
            email = self.request.POST['email']
            password = self.request.POST['password']

            if obj.get().email == email and obj.get().password == password:
                return super(LoginView, self).form_valid(form)
            else:
                messages.error(self.request, "invalid email or password")
                return self.form_invalid(form)
                # raise ValidationError("invalid email or password")
        else:
            messages.error(self.request, "invalid email or password")
            return self.form_invalid(form)
            # raise ValidationError("invalid email or password")

    def get_success_url(self):
        return reverse('dashboard_view')


class DashboardView(TemplateView):
    """to render the domain_form"""
    template_name = 'organization/dashboard.html'


class DemoView(View):
    """to render the domain_form"""
    template_name = 'organization/demo.html'

    def get(self, request, *args, **kwargs):
        host = request.META['HTTP_HOST']
        arr = host.split(".")
        host = arr[0]
        return render(request, self.template_name, {'hostname': host})

