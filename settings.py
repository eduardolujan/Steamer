import os
from django.conf import global_settings as default_settings

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_DEBUG = DEBUG = True

ADMINS = (('Admin', 'jfardello@uoc.edu'),)
SEND_BROKEN_LINK_EMAILS=False
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/mnt/ramdisk/djagios.db'
    }
}

TIME_ZONE = 'Europe/Madrid'

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = PROJECT_ROOT + "/media"
MEDIA_URL = "/media"

DJAGIOS_THEME = 'default'
DJAGIOS_EXP_PATH = PROJECT_ROOT + '/configs/export'
DJAGIOS_IMPORTENCODING = 'iso8859'
DJAGIOS_IMPORT_OBJECTS = ('NagiosCfg', 'TimePeriod', 'Command', 'Contact', 
                          'ContactGroup', 'Host', 'HostGroup', 'Service')
NAGIOS_PREFIX="/opt/local/nagios/"
STATIC_ROOT = PROJECT_ROOT + '/staticfiles/' 
STATIC_URL = '/static/'
GRAPPELLI_ADMIN_TITLE="The Nagios Config Creature from the Black Lagoon."
GRAPPELLI_INDEX_DASHBOARD = 'doctor.djagios.dashboard.DocDashboard'


ADMIN_MEDIA_PREFIX = STATIC_URL+'grappelli/'

STATICFILES_DIRS = ( PROJECT_ROOT + '/static/',)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = ''

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = default_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
)



MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'doctor.urls'

TEMPLATE_DIRS = (
        PROJECT_ROOT + "/tpl/"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django_evolution',
    'doctor.djagios',
)



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
            'verbose': {
                 'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
             },
            'simple': { 
                'format': '%(levelname)s %(message)s'
            },
    },
    'handlers': {
        'console':{ 
            'level':'DEBUG', 
            'class':'logging.StreamHandler', 
            'formatter': 'simple' 
            },
    },
    'loggers': {
        'django.request': { 'handlers': ['console'], 'level': 'ERROR', 'propagate': True, },
        'doctor.djagios.models': { 'handlers': ['console'], 'level': 'INFO', 'propagate': True, },
        'doctor.djagios.util': { 'handlers': ['console'], 'level': 'INFO', 'propagate': True, },
        'doctor.api.handlers': { 'handlers': ['console'], 'level': 'DEBUG', 'propagate': True, },
    }
}
