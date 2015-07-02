from .common import *

INSTALLED_APPS += ['debug_toolbar']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'volume', 'db.sqlite3'),
    }
}
