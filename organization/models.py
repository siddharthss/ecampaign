from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Organization(models.Model):
    organization_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200)
    pin = models.IntegerField()
    user = models.ForeignKey(User)
    domain_name = models.CharField(max_length=15, blank=True)


class Lead(models.Model):
    lead_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    pin = models.IntegerField()
    email = models.EmailField()
    country = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization)


class Campaign(models.Model):
    campaign_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    subject = models.CharField(max_length=100)
    content = RichTextField()
    filter = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization)

