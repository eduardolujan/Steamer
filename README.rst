Steamer
=======

Steamer is a tool for configuring nagios instances, it began as a fork of the `Djagios <http://djagios.org/>`_ project, with some added functionality, for instance, djagios was converted into a library and its tools were rewritten as django management commands, among bug fixes, and a re-bump of the djagios web-app which now uses django-piston as its ajax backend. 

**It is currently under heavy development, not yet documented, and _not yet ready for production_.**

Steamer was conceived for managing `Merlin-aware`<http://www.op5.org/community/plugin-inventory/op5-projects/merlin>`_ nagios clusters, it aims towards:

* A rewritten import tool
* Multiple nagios instances support
* Automated config deployment via [fabric](http://docs.fabfile.org/)
* Restful api for management.
* Web app for rapid editing template-based services and hosts

Stay tuned there's more to come! (And hopefully, some documentation )
        
