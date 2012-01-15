
ADMINS = (('Admin', 'admin@email'),)
MANAGERS = ADMINS
TIME_ZONE = 'Europe/Madrid'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'steamer.db'}}

#You may run "python manage.py genkey" to generate this value.
SECRET_KEY=''
