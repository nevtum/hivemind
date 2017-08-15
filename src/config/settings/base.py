"""
Django settings for echelon project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Attention!!
# Update this settings variable when releasing a new version of Echelon
# such as when there are changes to db models
RELEASE_VERSION = 'v0.6.3'

# Build paths inside the project like this: os.path.join(SRC_DIR, ...)
import os

SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(SRC_DIR)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'crispy_forms',
    'taggit',
]

ECHELON_APPS = [
    'common',
    'comments',
    'dirts',
    'accounts'
]

INSTALLED_APPS.extend(ECHELON_APPS)

from django.core.urlresolvers import reverse_lazy

APP_LINKS = [
    { 'title': 'Projects', 'url': reverse_lazy('common:projects') },
    { 'title': 'Issues', 'url': reverse_lazy('defects:list') },
]

# Import third party libraries
from .drf import *
from .haystack import *

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SRC_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.app_version',
                'config.context_processors.app_links',
                'config.context_processors.pending_registrations',                
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

SECRET_KEY = open(os.path.join(BASE_DIR, 'volume', 'secret_key.txt')).read()

ALLOWED_HOSTS = ['*']

LOGIN_URL = reverse_lazy('login-url')
LOGIN_REDIRECT_URL = reverse_lazy('home-url')

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(SRC_DIR, "static"),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'volume', 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}