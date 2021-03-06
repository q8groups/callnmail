import os

from django.db import models
from django.contrib.auth.models import User


class Mail(models.Model):
    user = models.ForeignKey(User)
    from_user = models.EmailField()
    to_user = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    date_email = models.DateTimeField()


    def __unicode__(self):
        return 'From: %s To: %s' %(self.from_user, self.to_user)



class MailAttachment(models.Model):
    mail = models.ForeignKey(Mail)
    attachment = models.FileField(upload_to='attachments/')

    def __unicode__(self):
        return "%s's mail attachment" %(self.mail.user)

    def filename(self):
        return os.path.basename(self.attachment.name)