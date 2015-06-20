from .common import *

SECRET_KEY = open(os.path.join(BASE_DIR, 'volume', 'secret_key.txt')).read()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'volume', 'db.sqlite3'),
    }
}
