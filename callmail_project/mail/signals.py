from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from advertisement.models import UserProfile


from rest_framework.authtoken.models import Token

from .models import ContactUs




