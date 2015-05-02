# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from .views import RegistrationView, PhoneNumberValidateView, MailView, LoginView, MailForwardView, UserProfileCreateView, CountryCreateView, ForgetPassword, ResetPassword, DeleteEmailLink, ChangePassword, AdvertismentBanner,PhoneNumberForgetPasswordValidateView

urlpatterns = patterns('',
                       url(r'^docs/', include('rest_framework_swagger.urls')),
                       url(r'^auth/', LoginView.as_view(), name='login'),
                       url(r'^register/$', RegistrationView.as_view(), name='user_registration'),
                       url(r'^validate-phone/$', PhoneNumberValidateView.as_view(), name='validate_phone'),
                       url(r'^validate-forget/$', PhoneNumberForgetPasswordValidateView.as_view(), name='validate_forget'),
                       url(r'^mail/$', MailView.as_view(), name='mail'),
                       url(r'^mail-forward/$', MailForwardView.as_view(), name='mail_forward'),
                       url(r'^mail-forward-destroy/$', DeleteEmailLink.as_view(), name='mail_forward_destroy'),
                       url(r'^user-profile/$', UserProfileCreateView.as_view(), name='user_profile_create'),
                       url(r'^country-code/$', CountryCreateView.as_view(), name='country_code'),
                       url(r'^forgot-password/$', ForgetPassword.as_view(), name='forgot_password'),
                       url(r'^forgot-password/(?P<secret_token>.+)/$', ResetPassword.as_view(), name='reset_password'),
                       url(r'^change-password/$', ChangePassword.as_view(), name='change_password'),
                       url(r'^ads/$', AdvertismentBanner.as_view(), name='banner'),





)






