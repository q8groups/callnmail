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



from dateutil import parser

from utils import send_sms


class FetchEmail:

    def __init__(self):
        self.HOST = 'localhost'
        self.USER = 'sachitad'
        self.PASSOWRD = 'devil'


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

            #Get the attachments
            for part in msg.walk():
                res =  part.get_content_type()
                print res
                if res == 'text/plain':
                    print part.get_payload(decode=True)
                #if part.get_content_maintype() == 'multipart':
                #    continue

                #if part.get('Content-Disposition') is None:
                #    continue


            self.server.store(message_id, '+FLAGS', '\\Deleted')

    def flush_emails(self):
        self.server.expunge()


#How to use:
server = FetchEmail()
server.login()
message_id = server.get_email_id()
if message_id:
    server.fetch_emails(message_id)
    server.flush_emails()


