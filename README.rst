Steamer
=======

Steamer is a tool for configuring nagios instances, it began as a fork of the [Djagios](http://djagios.org/) project, with some added functionality, for instance, djagios was converted into a library and its tools were rewriten as django management commands, among bugfixes, and a rebump of the djagios web-app which now uses django-piston as its ajax backend. 

**It is currently under heavy development, not yet documented, and _not yet ready for production_.**

Steamer was conceived for managing [merlin-aware](http://www.op5.org/community/plugin-inventory/op5-projects/merlin) nagios clusters, it aims to:

* A rewriten import tool
* Multiple nagios instances support
* Automated config deployment via [fabric](http://docs.fabfile.org/)
* Restfull api for management.
* Web app for rapid editing template-based sevices and hosts

stay tuned there's more to come! (And hopefully, some documentation )
        
