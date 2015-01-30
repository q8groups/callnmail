'''
Various utils for the mail application
'''

import random

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User


import magic

from twilio.rest import TwilioRestClient
from twilio import TwilioRestException



def send_sms(user, message):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.sms.messages.create(to=str(user), from_=settings.TWILIO_DEFAULT_CALLERID, body=message)
    except TwilioRestException:
        pass


def determine_mime_type(filepath):
    return magic.from_file(filepath, mime=True)


def generate_random_number():
    return random.randint(1000, 9999)


def create_random_password():
    from random import randint
    return "{0}".format(randint(1000, 9999))










# def mail_forward(from_, to, subject, body, attachment=None):
#     email = EmailMessage(subject, body, from_, to, headers = {'Reply-To': from_})
#     if attachment:
#         email.attach_file(attachment)
#     email.content_subtype = 'html'
#     email.send(fail_silently=False)


