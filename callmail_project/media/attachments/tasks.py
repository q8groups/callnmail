from datetime import timedelta

from celery import task

from mail_fetch import FetchEmail


@task
def email_cron():
    server = FetchEmail()
    server.login()
    message_id = server.get_email_id()

    if message_id:
        server.fetch_emails(message_id)
        #server.flush_emails()




CELERYBEAT_SCHEDULE = {
    'email_cron': {
        'task': 'tasks.email_cron',
        'schedule': timedelta(seconds=180),
    },
}

CELERY_TIMEZONE = 'UTC'