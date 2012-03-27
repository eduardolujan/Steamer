Rest API
========

Http requests
-------------

.. http:get:: /api/sample_uri/[?format=format&p=1&l=20]

    Every service accepts the ``format`` argument (django-piston default) and
    will try to authenticate via basic http authentication, or django
    authentication if the authorization header is not present.  So, a client
    should use the basic auth mechanism while browser's XMLHttpRequest client
    should include the django cookie header which its normally the default.

    Optionally the response can be paginated passing the ``p`` and ``l`` 
    parameters in the uri, if that's the case, the payload will be wrapped in
    a page object, and also a pager node will be appended to the response.

    **Example request**:

    .. sourcecode:: http

        GET /api/sample/uri/ HTTP/1.1
        Host: example.com
        Authorization: Basic cGVwZTpwZXBl
        Accept: application/json, text/javascript
        Content-Type: application/json

    :query format: one of ``json``, ``xml`` , defaults to ``json``
    :query p: page number, requires ``l`` , (enables pagination)
    :query l: entries per page, requires ``p``, (enables pagination)
    :statuscode 200: no error 
    :statuscode 201: created 
    :statuscode 204: deleted  
    :statuscode 400: Bad request 
    :statuscode 401: forbidden 
    :statuscode 410: gone 
    :statuscode 422: unprocessable (validation errors) 
    :statuscode 501: not implemented 
    :statuscode 503: throttled 
 

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Date: Wed, 08 Feb 2012 16:41:40 GMT
        Server: WSGIServer/0.1 Python/2.7
        Vary: Authorization, Cookie
        Content-Type: application/json; charset=utf-8


        [ { "id": "572b789d85354e06b0e62f7816c15f17", ...  }, { ....  }, ]


Services routing
----------------


 
.. http:get:: /api/service/

    Returns the service list.

.. http:get:: /api/service/<serviceid>/

    Returns detailed service information.

.. http:get:: /api/service/actions/getcmd/<serviceid>/<hostname>/

    Returns the exact command that nagios would run when checking this service.

.. http:get:: /api/service/forhost/<hostid>/ 

    Returns a list with the services that would run on a given host, solving
    hostgroups, and exclusions.

.. http:put:: /api/service/managehosts/[<serviceid>/]

    Based on the json payload, it will attach hosts, hostgroups, negated hosts,
    and negated groups to the service. Service can be given in the uri or in the payload as
    the ``service`` key.

    Payload args common for PUT & DELETE methods:

    ==================  ====================================================== 
      Arg                  Description               
    ==================  ====================================================== 
      **service**        Service ID if not present in the uri                 
      **host**           Host ID                                             
      **hostgroup**      Hostgroup ID                                         
      **host_n**         Negated host ID (translates to nagios ``"!host"``)   
      **hostgroup_n**    Negated hostgroup ID                                 
    ==================  ====================================================== 


    Example request:

    .. sourcecode:: http

        PUT /api/service/managehosts/ HTTP/1.1
        Host: example.com
        Content-Length: 88
        Content-Type: application/json
        Authorization: Basic cGVwZTpwZXBl
        
        {"service":"d80b43f274c9405b86a9ad0bda37d5ce","host":"735c1e3549f146efa9da74cc87afb933"}

.. http:delete:: /api/service/managehosts/[<serviceid>/]

    Based on the json payload, it will delete hosts, hostgroups, negated hosts,
    and negated groups from the service. Service can be given in the uri or in the payload as
    the ``service`` key. Payload keys are the same as in the PUT method.


Hosts routing
-------------


.. todo:: 

    This will be documented once the api freezes enough, there are plans
    to implement generalized linking (kinda' HATEOAS).

.. http:get:: /api/host/

.. http:get:: /api/host/templates/

.. http:get:: /api/host/<hostid>/

.. http:post:: /api/host/

.. http:delete:: /api/host/

.. http:put:: /api/host/

