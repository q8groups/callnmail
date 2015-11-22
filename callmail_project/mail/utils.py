'''
Various utils for the mail application
'''
import random
#import magic
import requests
import json
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


from celery import task



from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

from advertisement.models import UserProfile, Advertisement


from .models import MailForward






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


def send_notification(username,message):
    requests.packages.urllib3.disable_warnings()
    headers = {}
    headers['X-Parse-Application-Id']=settings.APPLICATION_ID
    headers['X-Parse-REST-API-Key']=settings.REST_API_KEY
    headers['Content-Type']='application/json'
    payload = {}
    payload["where"]={}
    payload["data"]={}
    payload["where"]["username"]=username
    payload["where"]["active"]=True
    payload["where"]["deviceType"]= {"$in":('ios','android')}
    payload["data"]["alert"]=message
    payload["data"]["sound"]="default"
    r = requests.post("https://api.parse.com/1/push",data=json.dumps(payload),headers=headers)
    json_data = json.loads(r.text)
    return json_data['result']


@task
def fetch_email(message):
    user_phonenumber = message.to_addresses[0].split('@')[0]
    domain = message.to_addresses[0].split('@')[1]
    if user_phonenumber[0]=='+' and domain=='callnmail.com':
        try:
            user = User.objects.get(username=user_phonenumber)
            if user.is_active is False:
                pass
            else:
                user_profile = UserProfile.objects.get(user=user)
                age = user_profile.age
                country = user_profile.country
                if age:
                    age_group = find_age_group(age)
                    advertisement = Advertisement.objects.filter(age_group=age_group,country=country)
                    if advertisement.exists():
                        try:
                            advertisementtext = advertisement[0].body + "<img src='"+advertisement.photo.url +"'/>"
                        except:
                            advertisementtext = advertisement[0].body
                    else:
                        advertisement = Advertisement.objects.get(default=True)
                        try:
                            advertisementtext = advertisement.body + "<img src='"+advertisement.photo.url +"'/>"
                        except:
                            advertisementtext = advertisement.body

                else:
                    advertisement = Advertisement.objects.get(default=True)
                    try:
                        advertisementtext = advertisement.body + "<img src='"+advertisement.photo.url +"'/>"
                    except:
                        advertisementtext = advertisement.body
                text_content = message.text + advertisementtext
                html_content = message.html + advertisementtext
                forward_email = MailForward.objects.filter(user=user)
                flag = forward_email.exists()
                if flag:
                    forward_email = forward_email.values_list('email')
                    forward_list = []
                    for i in forward_email:
                        for j in i:
                           forward_list.append(j)

                    subject = message.subject+' Via CallNMail'
                    from_email = message.from_address[0]
                    headers = {'Reply-To': message.from_address[0]}
                    msg = EmailMultiAlternatives(subject, text_content, from_email, forward_list,headers=headers)
                    for attachfile in message.attachments.all():
                        msg.attach(attachfile.get_filename(),attachfile.document.read(),attachfile.headers.split(';')[0].split(':')[1].strip())
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    send_notification(user.username,subject)
                    return "Sent Succesfully"
                return "User is not Active"
        except User.DoesNotExist:
            user = User.objects.create(username=user_phonenumber, is_active=False)
            user.set_unusable_password()
            user.userprofile.created_by_server=True
            user.userprofile.save()
            send_sms(user_phonenumber, settings.SMS_NEW_USER)
            return "User Created"

