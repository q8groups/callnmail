import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .utils import send_sms
from advertisement.models import UserProfile, Advertisement

from django_mailbox.signals import message_received
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Mail(models.Model):
    user = models.ForeignKey(User)
    from_user = models.EmailField()
    to_user = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    date_email = models.DateTimeField()

    def __unicode__(self):
        return 'From: %s To: %s' % (self.from_user, self.to_user)


class MailAttachment(models.Model):
    mail = models.ForeignKey(Mail)
    attachment = models.FileField(upload_to='attachments/')

    def __unicode__(self):
        return "%s's mail attachment" % (self.mail.user)

    def filename(self):
        return os.path.basename(self.attachment.name)


class ForgotPasswordToken(models.Model):
    user = models.ForeignKey(User)
    secret_token = models.IntegerField()


class MailForward(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()
    title= models.CharField(max_length=255)

    def __unicode__(self):
        return self.email

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
                advertisement = Advertisement.objects.filter(default=True)
                if advertisement.exists():
                    advertisement = advertisement[0].body
                else:
                    advertisement = Advertisement.objects.get(default=True)
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

                    subject = message.subject
                    from_email = message.to_addresses[0]
                    headers = {'Reply-To': message.from_address[0]}
                    msg = EmailMultiAlternatives(subject, text_content, from_email, forward_list,headers=headers)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    print "Email Sent"
        except User.DoesNotExist:
            user = User.objects.create(username=user_phonenumber, is_active=False)
            user.set_unusable_password()
            UserProfile.objects.create(user=user)
            send_sms(user_phonenumber, 'Yo new message waiting for ya, sign up.')
            print "SMS SENT"


@receiver(message_received)
def dance_jig(sender, message, **args):
    fetch_email(message)
    print "I just recieved a message titled %s from a mailbox named %s" % (message.subject, message.mailbox.name, )
