# Copyright (c) 2009 Jochen Maes
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
from django import forms

from fabric.context_managers import hide
from fabric.network import disconnect_all
from fabric.api import run, local, env

from doctor.djagios.models import *
from doctor.djagios.util import Syncer


def _sanitize_alias(name):
    return name.replace(' ', '_').lower()

@login_required
def home(request):
    t = loader.get_template('%s/home.html'%settings.DJAGIOS_THEME)
    # getting lists of hosts and their services
    hlist = Host.objects.exclude(register=False).order_by('host_name')
    c = RequestContext(request, {'hlist':hlist})
    return HttpResponse(t.render(c))

@permission_required('djagios.add_hosttemplate', login_url='/login')
def add_host_template(request):
    if request.method == 'POST':
        form = HostTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = HostTemplateForm()
    t = loader.get_template('%s/hosttemplateadd.html'%settings.DJAGIOS_THEME)
    c = RequestContext(request, {'form':form,})
    return HttpResponse(t.render(c))

@permission_required('djagios.add_host', login_url='/login')
def add_host(request):
    form = HostForm()
    tpl = '%s/hostadd.html' % settings.DJAGIOS_THEME
    c = RequestContext(request, {'form':form,})
    return render_to_response(tpl, context_instance=c)

@permission_required('djagios.delete_host', login_url='/login')
def delete_host(request):
    if request.method == 'POST':
        form = HostDeleteForm(request.POST)
        if form.is_valid():
            h = form.cleaned_data['host']
            h.delete()
            return HttpResponseRedirect('/')
    else:
        form = HostDeleteForm()
    t = loader.get_template('%s/hostdelete.html'%settings.DJAGIOS_THEME)
    c = RequestContext(request, {'form':form,})
    return HttpResponse(t.render(c))

@permission_required('djagios.change_service', login_url='/login')
def add_host_to_service(request):
    return _add_host_to_service(request, False)

@permission_required('djagios.change_host', login_url='/login')
def add_host_template_to_service(request):
    return _add_host_to_service(request, True)

def _add_host_to_service(request, template):
    if request.method == 'POST':
        form=None
        if template:
            form=HostTemplateToServiceForm(request.POST)
        else:
            form = HostToServiceForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data['service']
            h = form.cleaned_data['host']
            s.host_name.add(h)
            s.save()
            return HttpResponseRedirect('/')
    else:
        form=None
        t=None
        if template:
            form = HostTemplateToServiceForm()
            t = loader.get_template('%s/hosttemplateservice.html'%settings.DJAGIOS_THEME)
        else:
            form = HostToServiceForm()
            t = loader.get_template('%s/hostservice.html'%settings.DJAGIOS_THEME)
    c = RequestContext(request, {'form':form,})
    return HttpResponse(t.render(c))

@permission_required('djagios.change_service', login_url='/login')
def remove_host_from_service(request):
    return _remove_host_from_service(request,False)

@permission_required('djagios.change_host', login_url='/login')
def remove_host_template_from_service(request):
    return _remove_host_from_service(request,True)

def _remove_host_from_service(request,template):
    if request.method == 'POST':
        form=None
        if template:
            form=HostTemplateFromServiceForm(request.POST)
        else:
            form = HostFromServiceForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data['service']
            h = form.cleaned_data['host']
            if h in s.host_name.all():
                s.host_name.remove(h)
            else:
                s.host_name_n.add(h)
            s.save()
            return HttpResponseRedirect('/')
    else:
        form=None
        t=None
        if template:
            form = HostTemplateFromServiceForm()
            t = loader.get_template('%s/hosttemplateservice.html'%settings.DJAGIOS_THEME)
        else:
            form = HostFromServiceForm()
            t = loader.get_template('%s/hostservice.html'%settings.DJAGIOS_THEME)
    c = RequestContext(request, {'form':form, 'remove':True})
    return HttpResponse(t.render(c))


##################################
##### Helper methods
##################################

def get_general(request, exporttype, type, name):
    """Get the object requested if it exists.
    """
    type=type.lower()
    value=''
    o=None
    try:
        if type =='host':
            o = Host.get(name)
        elif type == 'hostgroup':
            o = HostGroup.get(name)
        elif type == 'service':
            o = Service.get(name)
        elif type == 'servicegroup':
            o = ServiceGroup.get(name)
        elif type == 'contact':
            o = Contact.get(name)
        elif type == 'contactgroup':
            o = ContactGroup.get(name)
        elif type == 'command':
            o = Command.get(name)
        elif type == 'checkcommand':
            o = CheckCommand.get(name)
        elif type == 'timeperiod':
            o == TimePeriod.get(name)
        elif type == 'timerange':
            o == TimeRange.get(name)
        elif type == 'servicedependency':
            o == ServiceDependency.get(name)
        elif type == 'cfgpath':
            o == CfgPath.get(name)
        else:
            txt="""ObjectType not Known: supported list:
    Host
    HostGroup
    Service
    ServiceGroup
    Contact
    Command
    CheckCommand
    TimePeriod
    TimeRange
    CfgPath
"""
            return HttpResponse(txt)
        value = serializers.serialize(exporttype,(o,))
        return HttpResponse(value, mimetype="application/javascript")
    except:
        return HttpResponse("Object not found")


@permission_required('djagios.change_service', login_url='/login')
def push_and_reload(request):
    sync = Syncer()
    sync.sync()
    sync.disconnect_all()
    json_ret=simplejson.dumps({'stderr':"",
                               'stdout':"\n".join(sync.sync_log),
                               'failed':False,
                               'succeeded':True}, indent=4)
    return HttpResponse(json_ret, mimetype="application/javascript")
