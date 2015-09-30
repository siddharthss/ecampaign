from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.generic import CreateView
from .forms import OrganizationRegistrationForm
from .models import Organization
# Create your views here.


class OrganizationRegistrationView(CreateView):
    model = Organization
    template_name = "organization/organization_registration.html"
    form_class = OrganizationRegistrationForm
    success_url = 'domain_form/'


class DomainFormView(TemplateView):
    """to render the template"""
    template_name = 'organization/domain_form.html'


class DomainFormValidationView(View):
    """to render organization registration form"""
    template_name = 'organization/thankyou.html'

    def post(self, request):
        domain_name = self.request.POST["domain_name"]
        return render(request, self.template_name, {'domain_name': domain_name})
