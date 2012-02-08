Rest API
========

Http requests
-------------

.. http:get:: /api/sample/uri/[?format=format]

    Every service accepts the ``format`` argument (django piston-default) and will try to autenticate
    against basic http authentication or django authentication (through the cookie session) if the
    authorization header is not presenti.  So, a client should use the basic auth mechanism while 
    browser's XMLHttpRequest client should include the django cookie header which its normally the default.

    **Example request**:

    .. sourcecode:: http

        GET /api/sample/uri/ HTTP/1.1
        Host: example.com
        Authorization: Basic cGVwZTpwZXBl
        Accept: application/json, text/javascript
        Content-Type: application/json


    :query format: one of ``json``, ``xml`` , defaults to ``json``
    :statuscode 200: no error 
    :statuscode 201: created 
    :statuscode 204: deleted  
    :statuscode 400: Bad request 
    :statuscode 401: forbidden 
    :statuscode 410: gone 
    :statuscode 422: unprossesable  
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

