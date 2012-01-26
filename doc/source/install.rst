
Installation
============

You will need to create a new virtual environment as a **non-root user**, if you're not used to virtual env here is the `documentation <http://www.virtualenv.org/en/latest/>`_ ::

    > virtualenv app 
    > cd app && . bin/activate
    > pip install django django-piston django-grappelli fabric django-uuidfield


Grab the code from github and name the root "steamer" ::

   > git clone git://github.com/jfardello/Steamer.git steamer && cd steamer


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
    


Initiate the database,  collect the app's `static files <https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>`_ for the httpd server, and generate a seed for django ::

    > ./manage.py syncdb
    > ./manage.py collectstatic
    > echo `./manage.py genkey` >> custom_settings.py


Deploy the app, you may want to refer to the `django docs <https://docs.djangoproject.com/en/dev/howto/deployment/>`_ , there's a template for running with apache and mod_wsgi on the misc directory ::

    >cp misc/steamer_wsgi.py ../bin/
    >cp misc/apache_sample /whatever/your/conf/is && vi !$

.. warning::
        Don't run the django site as the apache user especially if it is shared with other apps and steamer has ssh access to your services, if using mod_wsgi run the app as a daemon process and set the `user directive <http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIDaemonProcess>`_ ,  please see **securing steamer** for more info on the subject.   
    

That's it, restart your apache and you should be done.
Launch a web browser on whatever address your apache virtualhost listens, you should see at the root level the "Lite app", which won't do much till
you populate a little bit the database.  You should also see the admin dashboard at /admin.

