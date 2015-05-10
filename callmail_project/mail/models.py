import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import send_sms, find_age_group
from advertisement.models import UserProfile, Advertisement

from django_mailbox.signals import message_received
from rest_framework.authtoken.models import Token
from .tasks import fetch_email

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Mail(models.Model):
    user = models.ForeignKey(User)
    from_user = models.EmailField()
    to_user = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    date_email = models.DateTimeField()

    def __unicode__(self):
        return 'From: %s To: %s' % (self.from_user, self.to_user)


class AccountActivation(models.Model):
    user = models.ForeignKey(User)
    activation_code = models.IntegerField()
    is_done = models.BooleanField(default=False)


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
    is_done = models.BooleanField(default=False)


class MailForward(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.email


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __unicode__(self):
        return self.name



@receiver(message_received)
def dance_jig(sender, message, **args):
    fetch_email(message)
