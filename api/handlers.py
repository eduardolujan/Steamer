import re
import logging
from operator import or_

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db import transaction
from piston.handler import BaseHandler
from piston.utils import rc
from piston.utils import translate_mime
from piston.utils import MimerDataException

from steamer.djagios.models import *
logger = logging.getLogger(__name__)

__all__ = ['ServiceHandler', 'ServiceActions', 'TimePeriodHandler',
           'ListServiceHandler', 'HostHandler', 'CheckCommandHandler',
           'CommandHandler', 'ManageHostServices']


class ServiceHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT')
    model = Service
    fields = ('action_url', 'active_checks_enabled', 'check_command',
              'check_freshness', 'check_interval', 'check_period',
              'contact_groups', 'contacts', 'display_name', 'event_handler',
              'event_handler_enabled', 'first_notification_delay',
              'flap_detection_enabled', 'flap_detection_options',
              'freshness_threshold', 'high_flap_threshold', 'host_name',
              'host_name_n', 'hostgroup_name', 'hostgroup_name_n',
              'icon_image', 'icon_image_alt', 'id', 'initial_state',
              'is_volatile', 'low_flap_threshold', 'max_check_attempts',
              'name', 'notes', 'notes_url', 'notification_interval',
              'notification_options', 'notification_period',
              'notifications_enabled', 'obsess_over_service',
              'passive_checks_enabled', 'process_perf_data', 'register',
              'retain_nonstatus_information', 'retain_status_information',
              'retry_interval', 'service_description', 'servicegroups',
              'stalking_options', 'use', 'actions')

    @classmethod
    def actions(cls, service):
        kw = {'actionname': 'getcmd',
              'serviceid': service.pk,
              'extra': '%(HOSTNAME)s'}
        getcmd = reverse("service_actions", kwargs=kw)
        return {'get_cmd': {'method': 'GET', 'uri': getcmd}, }


class ServiceActions(BaseHandler):
    allowed_methods = ('GET')
    actions = ('getcmd')

    def read(self, request, actionname, serviceid, extra):
        if actionname in self.actions:
            try:
                action = getattr(Service.objects.get(pk=serviceid), actionname)
                return {actionname: action(extra)}
            except Service.DoesNotExist:
                return rc.BAD_REQUEST
        else:
            return rc.BAD_REQUEST


class ListServiceHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, hostid=None):
        '''Returns services for a host, taking care of templates and
        exclusions.'''

        if hostid is not None:
            host = Host.objects.get(pk=hostid)
            parents = [host, ] + host.get_parents()
            qobjs = []
            ex_qobjs = {}
            for each in parents:
                qobjs.append(Q(hostgroup_name__members=each))
                qobjs.append(Q(host_name=each))
                ex_qobjs['host_name_n'] = each
                ex_qobjs['hostgroup_name_n__members'] = each
            return Service.objects.filter(reduce(or_, qobjs))\
                        .exclude(**ex_qobjs).distinct().values(
                            'id',
                            'name',
                            'service_description',
                            'register')
        else:
            return Service.objects.all()\
                    .values('id', 'name', 'service_description', 'register')

class ManageHostServices(BaseHandler):
    allowed_methods = ('PUT', 'DELETE')

    def update(self, request, serviceid=None):
        return self._manage(request, serviceid=serviceid, action='add')

    def delete(self, request, serviceid=None):
        try:
            translate_mime(request)
            return self._manage(request, serviceid=serviceid, action='remove')
        except MimerDataException:
            return rc.BAD_REQUEST

    @transaction.commit_manually
    def _manage(self, request, serviceid=None, action='add'):
        allowed = ['host_name', 'host_name_n', 
                'hostgroup_name', 'hostgroup_name_n']
        if serviceid and request.content_type:
            data = request.data
            try:
                for key in allowed:
                    if isinstance(data.get(key), list) and \
                        len(data.get(key)) > 0 :
                        try:
                            if key.startswith('host_name'):
                                what = Host.objects.filter(
                                            host_name__in=data[key]).all() 
                            elif key.startswith('hostgroup_name'):
                                what = HostGroup.objects.filter(
                                            hostgroup_name__in=data[key]).all()
                            svc = Service.objects.get(pk=serviceid)
                            attr = getattr(svc, key) 
                            action = getattr(attr, action)
                            action(*what)
                            svc.save()
                        except Host.DoesNotExist:
                            return rc.BAD_REQUEST

                transaction.commit()
                return rc.ALL_OK
            except Exception, e:
                transaction.rollback()
                logger.error(e)
                return rc.BAD_REQUEST
        else:
            return rc.BAD_REQUEST

class TimePeriodHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = TimePeriod

    def read(self, request, id=None):
        '''Returns a single time_period if id is given, otherwise a subset.'''

        base = TimePeriod.objects
        if id:
            return base.get(pk=id)
        else:
            return base.all()


class HostHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'POST')
    model = Host
    exclude = ()

    def create(self, request):
        if request.content_type:
            data = request.data
            if data.get('use'):
                try:
                    data['use'] = Host.objects.get(id=data['use'])
                except Host.DoesNotExist:
                    return rc.BAD_REQUEST
            h = Host(**data)
            h.save()
            resp = rc.CREATED
            resp.write(" %s" % h.id)
            return resp
        else:
            super(HostHandler, self).create(request)

    def read(self, request, hostid=None, register=None):
        if register is not None:
            return Host.objects.filter(register=register)
        elif hostid is not None:
            return Host.objects.get(pk=hostid)
        else:
            return Host.objects.all()


class CheckCommandHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = CheckCommand


class CommandHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Command
