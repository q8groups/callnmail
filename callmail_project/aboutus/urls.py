# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from .views import Aboutus,Privacy,Terms,Broswer,Privacyandroid,Termsandroid,Aboutusandroid
urlpatterns = patterns('',
                       url(r'^privacy/$', Privacy, name='privacy'),
                        url(r'^terms/$', Terms, name='terms'),
                        url(r'^about-us/$', Aboutus, name='aboutus'),
                       url(r'^privacy/android/$', Privacyandroid, name='privacyandroid'),
                        url(r'^terms/android/$', Termsandroid, name='termsandroid'),
                        url(r'^about-us/android/$', Aboutusandroid, name='aboutusandroid'),
                        url(r'^browser/$', Broswer, name='browser'),





)






