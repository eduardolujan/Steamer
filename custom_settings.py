
ADMINS = (('Admin', 'admin@email'),)
MANAGERS = ADMINS
TIME_ZONE = 'Europe/Madrid'
DATABASES = {
            'default': {
                        'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/mnt/ramdisk/steamer.db'
                            }
            }

SECRET_KEY=''
