# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from .views import Aboutus,Privacy,Terms,Broswer
urlpatterns = patterns('',
                       url(r'^privacy/$', Privacy, name='privacy'),
                        url(r'^terms/$', Terms, name='terms'),
                        url(r'^about-us/$', Aboutus, name='aboutus'),
                        url(r'^browser/$', Broswer, name='browser'),





)






