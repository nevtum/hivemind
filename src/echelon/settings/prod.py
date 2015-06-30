from .common import *

SECRET_KEY = open(os.path.join(BASE_DIR, 'volume', 'secret_key.txt')).read()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Attention!!
# Update this settings variable when releasing a new version of Echelon
RELEASE_VERSION = 'v0.1.2'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'volume', 'db.sqlite3'),
    }
}
