#   Copyright (C) 2011, Jose Manuel Fardello.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import time
import datetime
import logging
from copy import deepcopy

from django.forms import Textarea
from django.contrib import admin
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.admin import FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.contrib import messages

from steamer.djagios.models import *
from steamer.djagios.util import Syncer, sync_status

logger = logging.getLogger(__name__)

class ChosenModelAdmin(admin.ModelAdmin):
    '''A custom ModelAdmin for overriding the admin/grappelli
    select boxes'''
    list_per_page = 50

    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static')
        js = [
              static_url + 'js/jquery.min.js',
               static_url + 'js/chosen.jquery.min.js',
               static_url + 'js/tiny_mce/tiny_mce.js',
               static_url + 'js/chosen.all.js']
        css = {"all": (static_url + 'css/chosen.css',
                        static_url + 'css/style-mce.css',)}


class DjagiosFlatPageAdmin(FlatPageAdmin, ChosenModelAdmin):
    formfield_overrides = {
            models.TextField: {
                'widget': Textarea(attrs={'cols': 120, 'rows': 50})},
    }


class HostAdmin(ChosenModelAdmin):
    list_display = ('alias', 'host_name', 'name', 'address')
    list_filter = ('alias',
                   'host_name',
                   'register',
                   'nagios_server__server_name')
    search_fields = ['alias', 'host_name', 'name', 'address']
    actions = ['attach_to_all_servers', ]

    def attach_to_all_servers(self, request, queryset):
        allservers = NagiosCfg.objects.all()
        for obj in queryset:
            obj.nagios_server = allservers
            obj.save()

    attach_to_all_servers.short_description = _("Attach the selected Hosts to \
            all nagios severs.")


class HostGroupAdminForm(forms.ModelForm):
    '''A custom ModelForm to prevent circular relations'''
    def __init__(self, *args, **kwargs):
        super(HostGroupAdminForm, self).__init__(*args, **kwargs)
        self.fields['hostgroup_members'].queryset = HostGroup.objects.exclude(
                hostgroup_name=self.instance.hostgroup_name)


class HostGroupAdmin(ChosenModelAdmin):
    list_display = ('alias', 'hostgroup_name')
    list_filter = ('members__host_name',
                   'hostgroup_members__members__host_name',
                   'hostgroup_name')
    form = HostGroupAdminForm


class NagiosCfgAdmin(ChosenModelAdmin):
    list_display = ('server_name', 'fabric_allow_deploy')
    actions = ['clone_model_instance', 'export_instance', ]

    def clone_model_instance(self, request, queryset):
        for obj in queryset:
            clonned_obj = deepcopy(obj)
            clonned_obj.id = None
            clonned_obj.server_name = "clonned.from.%s.at.%s" % (
                    obj.server_name,
                    int(time.mktime(datetime.datetime.now().timetuple()))
                    )
            clonned_obj.fabric_allow_deploy = False
            clonned_obj.save()

    clone_model_instance.short_description = _("Clone the selected items")

    def export_instance(self, request, queryset):
        if cache.add('push_lock', "true", settings.STEAMER_LOCK_EXPIRE):
            if queryset.count() > 0:
                ex_srvs = map(lambda s: s['server_name'], 
                              queryset.values('server_name'))
                logger.debug("Exporting: %s" % ex_srvs )
                self.sync = Syncer(server_name=ex_srvs)
                try:
                    self.sync.sync()
                    self.sync.disconnect_all()
                    succeed = True
                except Exception, e:
                    logger.error(e)
                    raise e 
                    succeed = False
                    messages.error(request, 'An error has been logged, please check the server log.')
                finally:
                    logger.debug(self.sync.status)
                    for server_name in self.sync.status.keys():
                        stat = self.sync.status[server_name]
                        if stat == sync_status['ROLLBACK_MADE']:
                            messages.error(request,
                                    '%s\'s config rolled back due to config validation errors.' % server_name)
                        elif stat == sync_status['ROLLBACK_FAILED']:
                            messages.error(request,
                                    'Failed rollback at %s\'s config, config may be unusable.' % server_name)
                        else:
                            method = "info" if self.sync.status[server_name] else "error"
                            message = "succeed" if self.sync.status[server_name] else "failed"
                            getattr(messages, method)(request, 'Export of %s %s' % (server_name, message))
                    cache.delete('push_lock')
        else:
            messages.error(request, 'Steamer server is currently exporting, please try again later.')
                
    export_instance.short_description = _("Export the selected servers configurations.")




class CfgPathAdmin(admin.ModelAdmin):
    pass


class CommandAdmin(admin.ModelAdmin):
    search_fields = ['command_name', 'command_line']


class CheckCommandAdmin(admin.ModelAdmin):
    pass


class ServiceAdmin(ChosenModelAdmin):
    list_display = ('service_description', 'name', 'use')
    list_filter = ('service_description', 
                   'name', 
                   'host_name', 
                   'host_name__nagios_server__server_name')
    search_fields = ('service_description', 'name',)


class ServiceGroupAdmin(admin.ModelAdmin):
    pass


class ContactAdmin(ChosenModelAdmin):
    pass


class ContactGroupAdmin(admin.ModelAdmin):
    pass


class TimePeriodAdmin(admin.ModelAdmin):
    pass


class TimeRangeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Host, HostAdmin)
admin.site.register(HostGroup, HostGroupAdmin)
admin.site.register(NagiosCfg, NagiosCfgAdmin)
admin.site.register(CfgPath, CfgPathAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(CheckCommand, CheckCommandAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceGroup, ServiceGroupAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactGroup, ContactGroupAdmin)
admin.site.register(TimePeriod, TimePeriodAdmin)
admin.site.register(TimeRange, TimeRangeAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, DjagiosFlatPageAdmin)
