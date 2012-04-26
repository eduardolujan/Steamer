# coding=utf8

# Copyright (c) 2012,  José Manuel Fardello
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from steamer import settings
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.core.cache import cache

from steamer.djagios.models import *
from steamer.djagios.util import Syncer
from steamer.api.forms import *

LOCK_EXPIRE = 120

@login_required
def home(request):
    t = loader.get_template('%s/home.html'%settings.STEAMER_THEME)
    # getting lists of hosts and their services
    hlist = Host.objects.exclude(register=False).order_by('host_name').values('id', 'host_name')
    c = RequestContext(request, {'hlist':hlist})
    return HttpResponse(t.render(c))


@permission_required('djagios.change_service', login_url='/login')
def push_and_reload(request):
    callback = request.GET.get('callback', '')
    if cache.add('push_lock', "true", LOCK_EXPIRE):
        sync = Syncer()
        try:
            sync.sync()
            sync.disconnect_all()
            retlog = "\n".join(sync.sync_log)
            succeed = True
        except Exception, e:
            retlog = e
            succeed = False
        finally:
            cache.delete('push_lock')
    else:
        succeed = False
        retlog = '''Someone is pushing a new configuration, please wait
                 while the lock gets released.'''

    json_ret=simplejson.dumps({'out':retlog, 'succeeded':succeed }, indent=4)
    json_ret = callback + '(' + json_ret + ');'
    return HttpResponse(json_ret, mimetype="application/javascript")


class SteamerTpl(TemplateView):
    '''Custom generic view, our app its just a bunch of ajax stuff pointing 
    to a piston api, this view loads the html, much more like the good ol'  
    direct_to_template view, it will add all forms to the context for 
    convenience '''
    extra = {}

    def __init__(self, *args, **kwargs):
        self.extra = kwargs.pop('extra', {})
        return super(SteamerTpl, self).__init__(*args, **kwargs)

    @method_decorator(permission_required('djagios.change_host'))
    def dispatch(self, *args, **kwargs):
        return super(SteamerTpl, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SteamerTpl, self).get_context_data(**kwargs)
        #Forms are just placeholders for our ajaxian stuff, we need no request,
        #as the endpoint is the piston api.
        context['forms'] = {'remove_host_from_service':RemoveHostFromServiceForm(),
                            'add_host_to_service':AddHostToServiceForm(),
                            'add_host':AddHostForm(),  
                            'remove_host':RemoveHostForm()}  
        context.update(self.extra)
        return context
