"""Development settings and globals."""

from __future__ import absolute_import

from os.path import join, normpath

from .base import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'callnmail',
        'USER': 'callnmail',
        'PASSWORD': 'noKia6230',
        'HOST': 'callnmail.ctgrepj1cb4h.eu-west-1.rds.amazonaws.com',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION



REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
   ),
   'PAGINATE_BY': 10,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        ),

    'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.JSONRenderer',

        )
}



# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
########## END TOOLBAR CONFIGURATION


EMAIL_SUBJECT_PREFIX = 'Callnmail Server'

SERVER_EMAIL = 'server@callnmail.com'
EMAIL_HOST_USER = SERVER_EMAIL




"""

EMAIL_SUBJECT_PREFIX = 'Callnmail Server'




EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'smtp.gmail.com'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = 'Nokia6230'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = 'mr.whos99@gmail.com'

SERVER_EMAIL = EMAIL_HOST_USER

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 587

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

"""

