from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
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
from .forms import OrganizationRegistrationForm
from .forms import DomainForm
from .forms import LoginForm
from .models import Organization

# Create your views here.


class OrganizationRegistrationView(FormView):
    # model = Organization
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
        organization_object = Organization.objects.create(organization_name=organization_name, address=address,
                                                       pin=pin, user_fk=user_object)
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
    form_class = LoginForm
    template_name = "organization/organization_login.html"

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                return super(LoginView, self).form_valid(form)
            else:
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

    def post(self, request):
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

