Notes on security
===================

.. warning::
    Steamer is not developed with security in mind and it may introduce lots of security related bugs while it is developed.


If you're planning to deploy steamer you should coinsider some points:

.. cssclass:: smalllist circle

    * Django should be run as a different user than the one runnng the web server, especially if the HTTP server is shared with other applications, if you are using apache mod_wsgi set the user and group keywords for the WSGIDaemonProcess directive.

    * Django root (python code) should be outside of the web server's root.

    * The Django user home should always be outside the web server root.

    * You should keep your SECRET_KEY secret.

    * Django does not throttle requests to authenticate users, if you do care about that, you should use a middleware, or your web server's throttling solution. 

    * There are some api calls that will create/edit check_commands, even prepending  nagios resource to the new command definition, it could be exploited by mallicious users, so, you should really trust the users who have access to the api, they will be literrally writing your nagios configuration.

    * A bad nagios configuration could lead to a self DoS attack.


