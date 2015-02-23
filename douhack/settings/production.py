from ._base import *
import os

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

RAVEN_CONFIG = {
    'dsn': os.environ.get('DSN'),
}

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

