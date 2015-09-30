from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.generic import FormView
from .forms import OrganizationRegistrationForm
from django.core.urlresolvers import reverse
from .models import Organization
# Create your views here.


class OrganizationRegistrationView(View):
    """to render organization registration form"""
    template_name = "organization/organization_registration.html"
    form_class = OrganizationRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, "organization/organization_registration.html", {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        return render(request, "organization/organization_registration.html", {'form': form})


# class OrganizationRegistrationValidateView(View):
#     """to validate organization registration form"""
#     form_class = OrganizationRegistrationForm
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             organization = form.save()
#             return render(request, 'organization/domain_form.html')
#         else:
#             return render(request, "organization/organization_registration.html", {'form': form})

class OrganizationRegistrationValidateView(FormView):

    form_class = OrganizationRegistrationForm
    success_url = 'domain_view'

    def form_valid(self, form):
        return super(OrganizationRegistrationValidateView, self).form_valid(form)


class DomainFormView(TemplateView):
    template_name = 'organization/domain_form.html'


class DomainFormValidationView(View):
    """to render organization registration form"""
    template_name = 'organization/thankyou.html'

    def post(self, request):
        domain_name = self.request.POST["domain_name"]
        return render(request, self.template_name, {'domain_name': domain_name})


