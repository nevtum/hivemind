from os import path

from .base import BASE_DIR, INSTALLED_APPS

INSTALLED_APPS += [
    'haystack'
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': path.join(BASE_DIR, 'volume', 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'