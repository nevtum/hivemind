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
RELEASE_VERSION = 'v0.2.10'

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
    'haystack',
]

ECHELON_APPS = [
    'common',
    'dirts',
    'accounts'
]

INSTALLED_APPS.extend(ECHELON_APPS)

from django.core.urlresolvers import reverse_lazy

APP_LINKS = [
    { 'title': 'Projects', 'url': reverse_lazy('projects') },
    { 'title': 'DIRTs', 'url': reverse_lazy('dirts-list') },
]

# Import third party libraries
from .drf import *

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'echelon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            SRC_DIR + '/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'echelon.context_processors.app_version',
                'echelon.context_processors.app_links',
                'echelon.context_processors.pending_registrations',                
            ],
        },
    },
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

WSGI_APPLICATION = 'echelon.wsgi.application'

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
