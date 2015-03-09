from django.contrib import admin

from .models import Mail, MailAttachment, MailForward, ForgotPasswordToken, AccountActivation, ContactUs

#admin.site.register(Mail)
#admin.site.register(MailAttachment)
admin.site.register(MailForward)
#admin.site.register(ForgotPasswordToken)
#admin.site.register(AccountActivation)
admin.site.register(ContactUs)