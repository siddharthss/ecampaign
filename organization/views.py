from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from .forms import OrganizationRegistrationForm
from .forms import DomainForm
from .models import Organization
# Create your views here.


class OrganizationRegistrationView(CreateView):
    model = Organization
    template_name = "organization/organization_registration.html"
    form_class = OrganizationRegistrationForm
    # success_url = 'domain_form/'

    def get_success_url(self):
        return reverse('domain_view', kwargs={'pk': self.object.id})


class DomainFormView(TemplateView):
    """to render the domain_form"""
    template_name = 'organization/domain_form.html'


# class DomainFormValidationView(UpdateView):
#     form_class = DomainForm
#     model = Organization
#     template_name = 'organization/domain_form.html'
#
#     def get(self, request, **kwargs):
#         self.object = Organization.objects.get(pk=self.request.pk)
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         context = self.get_context_data(object=self.object, form=form)
#         return self.render_to_response(context)
#
#     def get_object(self, queryset=None):
#         obj = Organization.objects.get(pk=self.request.pk)
#         return obj


class DomainFormValidationView(View):
    """to update/add  domain name in organization object """
    template_name = 'organization/thankyou.html'

    def post(self, request):
        domain_name = request.POST["domain_name"]
        pk = request.POST["pk"]
        obj = Organization.objects.get(pk=pk)
        obj.domain_name = domain_name
        obj.save()
        return render(request, self.template_name, {'domain_name': domain_name})
