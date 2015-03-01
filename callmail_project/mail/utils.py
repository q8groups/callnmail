'''
Various utils for the mail application
'''

import random

from django.conf import settings
from datetime import datetime

import magic

from twilio.rest import TwilioRestClient
from twilio import TwilioRestException


def send_sms(user, message):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.sms.messages.create(to=user, from_=settings.TWILIO_DEFAULT_CALLERID, body=message)
    except TwilioRestException:
        pass


def determine_mime_type(filepath):
    return magic.from_file(filepath, mime=True)


def generate_random_number():
    return random.randint(1000, 9999)


def create_random_password():
    from random import randint
    return "{0}".format(randint(1000, 9999))


def find_age_group(age):
    """
    :param age:
    :return: Return in which age group the age falls
    """
    todays_date = datetime.now().date()
    days = todays_date - age
    age = days.days/365

    if age in range(1, 6):
        group = '1-5'

    elif age in range(6, 15):
        group = '1-14'

    elif age in range(15, 26):
        group = '15-25'

    elif age in range(25, 46):
        group = '25-45'

    # We will support folks upto 110 years old only :)
    elif age in range(46, 111):
        group = '45+'

    else:
        group = None

    return group

# def mail_forward(from_, to, subject, body, attachment=None):
#     email = EmailMessage(subject, body, from_, to, headers = {'Reply-To': from_})
#     if attachment:
#         email.attach_file(attachment)
#     email.content_subtype = 'html'
#     email.send(fail_silently=False)


