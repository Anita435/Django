from .base import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'medico',
        'USER': 'medicouser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'deepakgariya0975@gmail.com'
EMAIL_HOST_PASSWORD = 'hxzplgwsrbdpiuur'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'deepakgariya0975@gmail.com'


SECRET_KEY = env('DJANGO_SECRET_KEY', default='bSG9EKqQ8WraxPRTudOkXZLQpJ6Mqy7i9bqiGjbqUTdgchkpcaJk5R74faP5hPMt')


DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

INTERNAL_IPS = ['127.0.0.1'] # for defining django-debug-toolbar
