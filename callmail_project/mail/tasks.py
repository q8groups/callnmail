from datetime import timedelta

from celery import task

from django_mailbox.models import Mailbox

@task
def email_cron():
    mailboxes = Mailbox.active_mailboxes.get('callnmail')
    mailboxes.get_new_mail()



