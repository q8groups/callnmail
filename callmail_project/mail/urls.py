from django.conf.urls import patterns, include, url

from .views import HomePage, RegistrationView, LoginView, MailListView, MailDetailView, download_attachment, PasswordResetView, PasswordResetRequestView, MailForwardCreateView, MailForwardListView, \
    AboutView, ActivateUser, ContactView, FAQView, PrivacyView, ProfileView, PasswordChangeView

urlpatterns = patterns('',
    url(r'^$', HomePage.as_view(), name='index'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^faq/$', FAQView.as_view(), name='faq'),
    url(r'^privacy/$', PrivacyView.as_view(), name='privacy'),
    url(r'^register/$', RegistrationView.as_view(), name='registration'),
    url(r'^activate/$', ActivateUser.as_view(), name='activate_user'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^mail/$', MailListView.as_view(), name='mail_list'),
    url(r'^mail/(?P<pk>\d+)/$', MailDetailView.as_view(), name='mail_detail'),
    url(r'^download/(?P<pk>\d+)/$', download_attachment, name='download_attachment'),
    url(r'^reset-password/$', PasswordResetView.as_view(), name='reset_password'),
    url(r'^reset-password-request/$', PasswordResetRequestView.as_view(), name='reset_password_request'),
    url(r'^change-password/$', PasswordChangeView.as_view(), name='change_password'),
    url(r'^mail-forward/$', MailForwardListView.as_view(), name='mailforward_list'),
    url(r'^mail-forward-create/$', MailForwardCreateView.as_view(), name='mailforward_create'),

)

