from ._base import *
import dj_database_url

DEBUG = True

INSTALLED_APPS += (
    'django_extensions',
    'django_nose',
    'debug_toolbar',
)

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://douhack@localhost/douhack'
    )
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    # '--cover-package=foo,bar',
]
