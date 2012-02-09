from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication 

from steamer.api.handlers import *
from steamer.api.auth import DjangoAuthentication 
from steamer.api.auth import MultiAuthentication 

auth = { 'authentication': MultiAuthentication([HttpBasicAuthentication(), DjangoAuthentication()])}


service_h = Resource(ServiceHandler, **auth)
services_forhost = Resource(ListServiceHandler, **auth)
host_h = Resource(HostHandler, **auth)
service_actions = Resource(ServiceActions, **auth)
manage_host_services = Resource(ManageHostServices, **auth)

urlpatterns = patterns('',
    url(r'^service/actions/(?P<actionname>\w+)/(?P<serviceid>\w+)/(?P<extra>.*)/$', service_actions, None, 'service_actions',),
    url(r'^service/forhost/(?P<hostid>\w+)/$', services_forhost),
    url(r'^service/managehosts/(?P<serviceid>\w+)/$', manage_host_services),
    url(r'^service/managehosts/$', manage_host_services),
    url(r'^service/(?P<id>[^/]+)/', service_h),
    url(r'^service/', service_h),
    url(r'^host/templates/$', host_h, {'register': False,}),
    url(r'^host/(?P<hostid>\w+)/$', host_h),
    url(r'^host/$', host_h),
)
