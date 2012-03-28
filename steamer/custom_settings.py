import os 

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
ADMINS = (('Admin', 'admin@email'),)
TIME_ZONE = 'Europe/Madrid'
DJAGIOS_IMP_DIR = PROJECT_ROOT + "/cfg/import"
DJAGIOS_EXP_DIR = PROJECT_ROOT + "/cfg/export"
DATABASES = {'default': {
                'ENGINE': 'django.db.backends.sqlite3', 
                'NAME': '%s/db/steamer.db' % PROJECT_ROOT } }
