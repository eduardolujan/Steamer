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

Admonition
==========

This software is **not yet ready for production use**, it is currently in alpha stage.

Description: An effortless system for monitoring provisioning. 
==============================================================
 
/ˈstēmər/: A tool for provisioning monitoring services across multiple nagios instances, an in-progress attempt to automate the management of large `merlin-aware <http://www.op5.org/community/plugin-inventory/op5-projects/merlin>`_ nagios installations.


The project aims towards:
    * Automating nagios configuration generation
    * Centralize nagios config definitions.
    * Automate nagios config deployment with rollback capabilities.
    * Restfull api for quick integration. 
    * Import tools. 
 
 
Yet another nagios creature?
============================

Yes, there's plenty of them, and yes, they all work. If you're looking for a nagios gui tool, consider `centreon <http://www.centreon.com/>`_, `pynag <http://code.google.com/p/pynag/>`_, `djagios <http://djagios.org/>`_, `nconf <http://sourceforge.net/projects/nconf/>`_.

This project exists because of the author's need for a (preferably pythonic) nagios provisioning solution through rest web services. Steamer uses a modified djagios version as its django data model, the original, by Jochen Maes, was written with a single instance in mind, the one steamer uses was converted to a module and twicked up a little.


How it works
============
 
Steamer has a repository for all your nagios directives, services, hosts, its dependencies are related with "server instances". Based on that data it generates the configuration which gets pushed via ssh to each managed nagios servers. It has a simple web app for showing some basic information and for basic template based editing, a django-admin site, and a piston api which exposes all the admin functionality.

