from django.contrib import admin

from .models import Mail, MailAttachment, MailForward, ForgotPasswordToken, AccountActivation, ContactUs

class MailForwardAdmin(admin.ModelAdmin):
    list_display = ("email","user__username")
    search_fields = ("email","user__username")


#admin.site.register(Mail)
#admin.site.register(MailAttachment)
admin.site.register(MailForward,MailForwardAdmin)
#admin.site.register(ForgotPasswordToken)
#admin.site.register(AccountActivation)
admin.site.register(ContactUs)