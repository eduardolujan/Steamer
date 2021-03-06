
Installation
============

You will need to create a new virtual environment as a **non-root user**, if you're not used to virtual env here is the `documentation <http://www.virtualenv.org/en/latest/>`_ . It's assumed that the system account is exclusively used by steamer.

.. code-block:: sh

    > sudo apt-get install python-dev python-mysqldb libapache2-mod-wsgi
    > cd ~/.. && virtualenv --system-site-packages $(basename ~) 
    > cd && . bin/activate
    > pip install django==1.3 django-grappelli==2.3.8 fabric django-uuidfield chardet


Grab the code from github. 

.. code-block:: sh

   > git clone git://github.com/jfardello/Steamer.git app  && cd app


Edit your database settings:

:file: `custom_settings.py`


.. code-block:: python

    import os

    PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
    ADMINS = (('Admin', 'admin@email'),)
    TIME_ZONE = 'Europe/Madrid'
    DJAGIOS_IMP_DIR = PROJECT_ROOT + "/cfg/import"
    DJAGIOS_EXP_DIR = PROJECT_ROOT + "/cfg/export"
    DATABASES = {'default': {
                    'ENGINE': 'django.db.backends.sqlite3', 
                    'NAME': '%s/db/steamer.db' % PROJECT_ROOT } }
    

.. note:: Take a look `here <https://docs.djangoproject.com/en/1.4/ref/settings/#databases>`_ for information on your specific db backend.


Initiate the database,  collect the app's `static files <https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>`_ for the httpd server, and generate a seed for django ::

    > ./manage.py syncdb
    > ./manage.py createcachetable locking_backend
    > ./manage.py collectstatic
    > echo `./manage.py genkey` >> custom_settings.py


Deploy the app, you may want to refer to the `django docs <https://docs.djangoproject.com/en/dev/howto/deployment/>`_ , there's a template for running with apache and mod_wsgi on the misc directory ::

    >cp steamer/wsgi.py ../bin/
    #cp misc/steamer.conf.sample /whatever/your/conf/is 

**Review** and **edit** wsgi.py and the apache configuration.

.. warning::
        Don't run the django site as the apache user especially if it is shared with other apps and steamer has ssh access to your services, if using mod_wsgi run the app as a daemon process and set the `user directive <http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIDaemonProcess>`_ ,  please see :doc:`sec` for more info on the subject.   
    

That's it, restart your apache and you should be done.
Launch a web browser on whatever address your apache virtualhost listens, you should see at the root level the "Lite app", which won't do much till
you populate a little bit the database.  You should also see the admin dashboard at /admin.


