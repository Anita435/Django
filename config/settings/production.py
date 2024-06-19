from .base import *
from .base import env

DEBUG = False

SECRET_KEY = 'oe&dzt#v*%8*nxac+%t-cnt=6(9r2d!qh0h9g@go48%+dhzp8g'

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECRET_KEY = env('DJANGO_SECRET_KEY')
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['3.17.159.241'])

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'admin',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

LOGGING = {

    'version': 1,

    'disable_existing_loggers': True,

    'formatters': {

        'verbose': {

            'format': '%(levelname)s [%(asctime)s] %(module)s %(message)s'

        },

    },

    'handlers': {

        'console': {

            'level': 'DEBUG',

            'class': 'logging.StreamHandler',

            'formatter': 'simple'

        },

        'file': {

            'class': 'logging.handlers.RotatingFileHandler',

            'formatter': 'verbose',

            'filename': '/var/www/logs/ibiddjango.log',

            'maxBytes': 1024000,

            'backupCount': 3,

        },

        'mail_admins': {

            'level': 'ERROR',

            'class': 'django.utils.log.AdminEmailHandler'

        }

    },

    'loggers': {

        'django': {

            'handlers': ['file', 'console', 'mail_admins'],

            'propagate': True,

            'level': 'DEBUG',

        },

    }

}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'deepakgariya0975@gmail.com'
EMAIL_HOST_PASSWORD = 'hxzplgwsrbdpiuur'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'deepakgariya0975@gmail.com'


SEND_BROKEN_LINK_EMAILS = True
ADMINS = [('deepak', 'deepakgariya0975@gmail.com')]
