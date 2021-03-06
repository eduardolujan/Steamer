.. Steamer Documentation.

#######################
Steamer's Documentation
#######################

.. toctree::
   :maxdepth: 2
   
   install
   config
   web
   api
   sec
   appendix


.. cssclass:: dtable

    .. warning ::

        This software is **not yet ready for production use**, it is currently in alpha stage.

An effortless system for monitoring provisioning. 
=================================================
 
/ˈstēmər/: A tool for provisioning monitoring services across multiple nagios instances, an in-progress attempt to automate the management of large `merlin-aware <http://www.op5.org/community/plugin-inventory/op5-projects/merlin>`_ nagios installations.


The project aims towards:
    * Automating nagios configuration generation
    * Centralize nagios config definitions.
    * Automate nagios config deployment with rollback capabilities.
    * Restfull api for quick integration. 
    * Importing tools. 
 
 
Yet another nagios creature?
============================

Yes, there's plenty of them, and yes, they all work. If you're looking for a nagios gui tool, consider `centreon <http://www.centreon.com/>`_, `pynag <http://code.google.com/p/pynag/>`_, `djagios <http://djagios.org/>`_, `nconf <http://sourceforge.net/projects/nconf/>`_.

This project exists because of the author's need for a (preferably pythonic) nagios provisioning solution through rest web services. Steamer uses a modified djagios version as its django data model, the original, by Jochen Maes, was written with a single instance in mind, the one steamer uses was converted to a module and twicked up a little.


How it works
============
 
Steamer has a repository for all your nagios directives, services, hosts and its dependencies which are are related to "server instances". Based on that data and relations Steamer is able to generate the configuration for each managed server which gets pushed to it through ssh. It has a simple web app for showing some basic information and for basic template based editing, a full-featured django-admin site, and a piston api which exposes all the admin functionality.

