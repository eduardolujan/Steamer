from django.conf.urls.defaults import *
from piston.resource import Resource

from doctor.api.handlers import *

service_h = Resource(ServiceHandler)
list_service_h = Resource(ListServiceHandler)
host_h = Resource(HostHandler)

urlpatterns = patterns('',
    url(r'^service/forhost/(?P<hostid>\w+)/$', list_service_h),
    url(r'^service/(?P<id>[^/]+)/', service_h),
    url(r'^service/', list_service_h),
    url(r'^host/templates/$', host_h, {'register':False,}),
    url(r'^host/(?P<hostid>\w+)/$', host_h),
    url(r'^host/$', host_h),
)
