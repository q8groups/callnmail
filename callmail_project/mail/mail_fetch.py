'''
1. Configure postfix to accept non existent system level users
2. Forward all the e-mails to the superuser: sachitad@localhost
3. Configure Postfix with IMAP to read the e-mails
4. Use the python standard library to get the emails and store in the database
5. Once the email is stored in the database flush all the emails
'''
import os
import email
import imaplib
from pytz import timezone


from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.base import File
from django.core.mail import EmailMessage, EmailMultiAlternatives



from dateutil import parser

from .models import Mail, MailAttachment, MailForward
from advertisement.models import UserProfile, Advertisement
from .utils import send_sms


class FetchEmail:

    def __init__(self):
        self.HOST = 'localhost'
        self.USER = 'callnmail'
        self.PASSOWRD = 'redhat123'

    def login(self):
        self.server = imaplib.IMAP4(self.HOST)
        self.server.login(self.USER, self.PASSOWRD)

    def get_email_id(self):
        self.server.select('INBOX')
        messages = self.server.search(None, '(UNSEEN)')   #Format would be like ('OK', ['1 2 3 4 5 6 7 8'])

        if messages[1][0] == '0' or messages[1][0] == '':       # Means there are no new emails
            messages_id = None

        else:
            messages_id = ', '.join(messages[1]).split(' ')

        return messages_id

    def fetch_emails(self, messages_ids):
        for message_id in messages_ids:
            status, msg_data = self.server.fetch(message_id, '(RFC822)')
            msg = email.message_from_string(msg_data[0][1])
            body = msg.get_payload(decode=True)
            if body:
                body_message = body.rstrip()
            else:
                body_message = None

            subject = msg['subject']
            from_email = msg['from']
            to_email = msg['X-Original-To']
            date_email = parser.parse(msg['date']).astimezone(timezone('UTC'))

            user_phonenumber = to_email.split('@')[0]

            try:
                user = User.objects.get(username=user_phonenumber)
                if user.is_active is False:
                    send_sms(user_phonenumber, 'Yo new message waiting for ya, sign up.')
                else:
                    user_profile = UserProfile.objects.get(user=user)
                    advertisement = Advertisement.objects.filter(default=True)
                    if advertisement.exists():
                        advertisement = advertisement[0].body
                    else:
                        advertisement = Advertisement.objects.get(default=True)
                        advertisement = advertisement.body
                    if body_message:
                        body_message = body_message + advertisement
            except User.DoesNotExist:
                user = User.objects.create(username=user_phonenumber, is_active=False)
                user.set_unusable_password()
                UserProfile.objects.create(user=user)
                send_sms(user_phonenumber, 'Yo new message waiting for ya, sign up.')


            object = Mail.objects.create(user=user, subject=subject, from_user=from_email, body=body_message, to_user=to_email, date_email=date_email)


            forward_email = MailForward.objects.filter(user=user)
            flag = forward_email.exists()
            if flag:
                forward_email = forward_email.values_list('email')
                forward_list = []
                for i in forward_email:
                    for j in i:
                        forward_list.append(j)

                mail_forward = EmailMessage(subject, body_message, from_email, forward_list, headers = {'Reply-To': from_email})

            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).rstrip()
                    object.body = body
                    object.save()

                if part.get_content_maintype() == ' multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                if flag:
                    mail_forward = EmailMessage(subject, body+advertisement, from_email, forward_list, headers = {'Reply-To': from_email})




                filename = part.get_filename()
                att_path = os.path.join(settings.MEDIA_ROOT, filename)
                temporary_file = open(att_path, 'wb')
                temporary_file.write(part.get_payload(decode=True))
                temporary_file.close()

                file_ = File(file(att_path))
                MailAttachment.objects.create(mail=object, attachment=file_)

                if flag:
                    mail_forward.attach_file(att_path)
                os.remove(os.path.join(settings.MEDIA_ROOT, filename))

            if flag:
                mail_forward.content_subtype = 'html'
                mail_forward.send(fail_silently=False)

    def flush_emails(self):
        self.server.expunge()







# #How to use:
# server = FetchEmail()
# server.login()
# message_id = server.get_email_id()
# if message_id:
#     server.fetch_emails(message_id)
#     server.flush_emails()


