from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    address = models.CharField(max_length=200)
    pin = models.IntegerField()
    domain_name = models.CharField(max_length=15, blank=True, unique=True)


class Lead(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    pin = models.IntegerField()
    email = models.EmailField()
    country = CountryField()


class Rule(models.Model):
    source = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    operator = models.CharField(max_length=100)


class Campaign(models.Model):
    organization = models.ForeignKey(Organization)
    rule = models.ForeignKey(Rule)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    subject = models.CharField(max_length=100)
    content = RichTextField()


class ScheduleLog(models.Model):
    campaign = models.ForeignKey(Campaign)
    lead = models.ForeignKey(Lead)
    send_at = models.DateTimeField()

