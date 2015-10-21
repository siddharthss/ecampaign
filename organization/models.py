from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Organization(models.Model):
    organization_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200)
    pin = models.IntegerField()
    user_fk = models.ForeignKey(User)
    domain_name = models.CharField(max_length=15, blank=True)
