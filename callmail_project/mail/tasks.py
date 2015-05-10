from datetime import timedelta

from celery import task

from django_mailbox.models import Mailbox,Message
from django.core.mail import EmailMultiAlternatives
from advertisement.models import UserProfile, Advertisement
from django.contrib.auth.models import User

from .models import MailForward
from .utils import send_sms,find_age_group

@task
def email_cron():
    mailboxes = Mailbox.active_mailboxes.all()[0]
    mailboxes.get_new_mail()

@task
def fetch_email(message):
    user_phonenumber = message.to_addresses[0].split('@')[0]
    domain = message.to_addresses[0].split('@')[1]
    if user_phonenumber[0]=='+' and domain=='callnmail.com':
        try:
            user = User.objects.get(username=user_phonenumber)
            if user.is_active is False:
                pass
                #send_sms(user_phonenumber, 'Yo new message waiting for ya, sign up.')
            else:
                user_profile = UserProfile.objects.get(user=user)
                age = user_profile.age
                if age:
                    age_group = find_age_group(age)
                    advertisement = Advertisement.objects.filter(age_group=age_group)
                    if advertisement.exists():
                        advertisement = advertisement[0].body
                    else:
                        advertisement = Advertisement.objects.get(default=True)
                        advertisement = advertisement.body

                else:
                    advertisement = Advertisement.objects.get(default=True)
                    #uadvertisement = '<img src="'+advertisement.photo.url+'"/>'
                    advertisement = advertisement.body

                text_content = message.text + advertisement
                html_content = message.html + advertisement
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
        except User.DoesNotExist:
            user = User.objects.create(username=user_phonenumber, is_active=False)
            user.set_unusable_password()
            user.userprofile.created_by_server=True
            user.userprofile.save()
            send_sms(user.username, 'Yo new message waiting for ya, sign up.')





@task
def sendSavedMails(user):
    email = str(user.username)+'@callnmail.com'
    for e in Message.objects.filter(to_header__contains=email):
        fetch_email(e)





