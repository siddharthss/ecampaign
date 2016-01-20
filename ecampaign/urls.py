"""ecampaign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from organization.views import DemoView
from organization.views import LoginView
from organization.views import DashboardView

urlpatterns = [
    url(r'^$', DemoView.as_view()),
    url(r'^organization/', include('organization.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', LoginView.as_view(), name='login_view'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard_view'),
    url(r'^schedule/', include('schedule.urls')),
]
