from decouple import config

from .base import *


DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

import socket

ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1']
