from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from celery import task

from django_mailbox.models import Mailbox,Message
from .utils import fetch_email

@task
def email_cron():
    mailboxes = Mailbox.active_mailboxes.all()[0]
    mailboxes.get_new_mail()

@task
def email_clean():
    m = Message.objects.filter(processed__lte= timezone.now()-timedelta(days=settings.MAIL_CLEAN_PERIOD))
    count = m.count()
    m.delete()
    return count


@task
def sendSavedMails(user):
    email = str(user.username)+'@callnmail.com'
    for e in Message.objects.filter(to_header__contains=email):
        fetch_email.delay(e)
    return True








