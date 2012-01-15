from django.conf.urls.defaults import *
from piston.resource import Resource

from steamer.api.handlers import *
from steamer.api.auth import DjangoAuthentication

auth = DjangoAuthentication()

service_h = Resource(ServiceHandler, authentication=auth)
list_service_h = Resource(ListServiceHandler, authentication=auth)
host_h = Resource(HostHandler, authentication=auth)
service_actions = Resource(ServiceActions, authentication=auth)
manage_host_services = Resource(ManageHostServices, authentication=auth)

urlpatterns = patterns('',
    url(r'^service/actions/(?P<actionname>\w+)/(?P<serviceid>\w+)/(?P<extra>.*)/$', service_actions, None, 'service_actions',),
    url(r'^service/forhost/(?P<hostid>\w+)/$', list_service_h),
    url(r'^service/managehosts/(?P<serviceid>\w+)/$', manage_host_services),
    url(r'^service/(?P<id>[^/]+)/', service_h),
    url(r'^service/', list_service_h),
    url(r'^host/templates/$', host_h, {'register': False,}),
    url(r'^host/(?P<hostid>\w+)/$', host_h),
    url(r'^host/$', host_h),
)
