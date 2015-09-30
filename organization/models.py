from django.db import models

# Create your models here.


class Organization(models.Model):
    organization_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200)
    pin = models.IntegerField()
    user_first_name = models.CharField(max_length=100)
    user_last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=100)
