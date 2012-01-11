from django.conf.urls.defaults import *
from piston.resource import Resource

from doctor.api.handlers import *

service_h = Resource(ServiceHandler)
list_service_h = Resource(ListServiceHandler)
host_h = Resource(HostHandler)
service_actions = Resource(ServiceActions)

urlpatterns = patterns('',
    url(r'^service/actions/(?P<actionname>\w+)/(?P<serviceid>\w+)/(?P<extra>.*)/$', service_actions, None, 'service_actions',),
    url(r'^service/forhost/(?P<hostid>\w+)/$', list_service_h),
    url(r'^service/(?P<id>[^/]+)/', service_h),
    url(r'^service/', list_service_h),
    url(r'^host/templates/$', host_h, {'register':False,}),
    url(r'^host/(?P<hostid>\w+)/$', host_h),
    url(r'^host/$', host_h),
)
