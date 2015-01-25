from django.db import models
from django.contrib.auth.models import User


class TokenValidation(models.Model):
    """
    Validation Token for user -- when user is created!
    """
    user = models.ForeignKey(User)
    secret_token = models.IntegerField()


class Country(models.Model):
    """
    Country Model for list View
    """
    code = models.CharField(max_length=4,primary_key=True)
    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=6,blank=True)
    priority = models.PositiveSmallIntegerField(default=0)