import os
from django.conf import global_settings as default_settings
try:
    from custom_settings import *
except:
    pass

MANAGERS = ADMINS

DEBUG = False
TEMPLATE_DEBUG = False

APPEND_SLASH = True
SEND_BROKEN_LINK_EMAILS=False
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = PROJECT_ROOT + "/media"
MEDIA_URL = "/media"

STEAMER_THEME = 'default'
STEAMER_EXP_PATH = PROJECT_ROOT + '/cfg/export'
STEAMER_IMPORTENCODING = 'iso8859'
STEAMER_KEY_FILE="~/.ssh/id_steamer_dsa.pub"
STEAMER_LOCK_EXPIRE = 120
STEAMER_RESTART_NAGIOS = False
NAGIOS_PREFIX="/opt/local/nagios/"
STATIC_ROOT = PROJECT_ROOT + '/staticfiles/' 
STATIC_URL = '/static/'
GRAPPELLI_ADMIN_TITLE="Steamer admin"
GRAPPELLI_INDEX_DASHBOARD = 'steamer.djagios.dashboard.DocDashboard'

STEAMER_IMPORT_OBJECTS = ('NagiosCfg', 'TimePeriod', 'Command', 'Contact', 
                          'ContactGroup', 'Host', 'HostGroup', 'Service')

ADMIN_MEDIA_PREFIX = STATIC_URL+'grappelli/'

STATICFILES_DIRS = ( PROJECT_ROOT + '/static/',)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = default_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'locking_backend',
    }
}



MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'steamer.urls'

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
    #'django_evolution',
    'steamer.djagios',
    #'debug_toolbar',
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
        'steamer.djagios.models': { 'handlers': ['console'], 'level': 'ERROR', 'propagate': True, },
        'steamer.djagios.util': { 'handlers': ['console'], 'level': 'ERROR', 'propagate': True, },
        'steamer.djagios.admin': { 'handlers': ['console'], 'level': 'ERROR', 'propagate': True, },
        'steamer.api.handlers': { 'handlers': ['console'], 'level': 'ERROR', 'propagate': True, },
    }
}
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = { 'INTERCEPT_REDIRECTS': False,}
