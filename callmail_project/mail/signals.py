from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from advertisement.models import UserProfile, Advertisement


from rest_framework.authtoken.models import Token

from .models import ContactUs
@receiver(post_save, sender=ContactUs)
def SendEmailContactUs(sender, instance=None, created=False, **kwargs):
    if created:
        msg = EmailMultiAlternatives(instance.subject, instance.message, instance.contact_email, ['contact@callnmail.com',])
        msg.send()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)

