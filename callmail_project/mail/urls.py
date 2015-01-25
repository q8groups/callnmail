from django.conf.urls import patterns, include, url

from .views import HomePage, RegistrationView, LoginView, MailListView, MailDetailView, download_attachment, PasswordResetView, PasswordResetRequestView, MailForwardCreateView, MailForwardListView

urlpatterns = patterns('',
    url(r'^$', HomePage.as_view(), name='index'),
    url(r'^register/$', RegistrationView.as_view(), name='registration'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^mail/$', MailListView.as_view(), name='mail_list'),
    url(r'^mail/(?P<pk>\d+)/$', MailDetailView.as_view(), name='mail_detail'),
    url(r'^download/(?P<pk>\d+)/$', download_attachment, name='download_attachment'),
    url(r'^reset-password/$', PasswordResetView.as_view(), name='reset_password'),
    url(r'^reset-password-request/$', PasswordResetRequestView.as_view(), name='reset_password_request'),
    url(r'^mail-forward/$', MailForwardListView.as_view(), name='mailforward_list'),
    url(r'^mail-forward-create/$', MailForwardCreateView.as_view(), name='mailforward_create'),

)

