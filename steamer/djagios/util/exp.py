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

import os
import sys
import shutil
import logging
import time
import datetime

from fabric.context_managers import hide
from fabric.context_managers import settings as stts
from fabric.network import disconnect_all
from fabric.api import run, local, env
from fabric.contrib.project import rsync_project
from django.db.models import Q

from steamer import settings
from steamer.djagios.models import *

logger = logging.getLogger(__name__)

sync_status = {'ROLLBACK_MADE': -1,
               'ROLLBACK_FAILED': -2}

class Exporter():
    """Exporter provides the functionality to export the different objects to the correct format
    used by Nagios.
    This tool will have to be adapted each time the configuration format of Nagios changes.
    """

    def _write_file(self, content, path):
        """Internal function that will write out the string to a file.
        """
        logger.debug("Exporter._write_file: opening %s"%path)
        if os.path.exists(path) and not os.path.isfile(path):
            logger.error("Exporter._write_file: %s is not a file"%path)
            return
        file = open(path, 'a')
        file.write(content)
        file.flush()
        file.close()
        logger.debug("Exporter._write_file: closed %s"%path)

    def export(self, path, nagios_server=None):
        """export will run over all objects and export them one by one to the specified 
        path. Here they will be ordered per objecttype.
        The export is not recursive.

        :param path: containing the location where to put the cfg files, **must be a directory**
        :type path: :class:`str`
        """
        if not os.path.isdir(path):
            raise ValueError('given path %s is not a directory!'%path)

        # creating the objects dir
        objs_dir=os.path.join(path, 'objects')
        if os.path.exists(objs_dir):
            shutil.rmtree(objs_dir)
            os.mkdir(objs_dir)
        # removing previous nagios.cfg
        if os.path.exists(os.path.join(path, 'nagios.cfg')):
            os.remove(os.path.join(path, 'nagios.cfg'))
        
        OBJECT_LIST = (Host, HostGroup, Service, ServiceGroup, Command, TimePeriod,\
                Contact, ContactGroup,)
        for o in OBJECT_LIST:
            if o.__name__ is 'Host':
                #Filter hosts pointing to our nagios server destination.
                objs = o.objects.distinct(Q(nagios_server__server_name=nagios_server) | Q(register=False))
            elif o.__name__ is 'Service':
                #Filter services used in hosts pointing to our nagios server destination.
                objs = o.objects.distinct(
                        
                      Q(Q(host_name__nagios_server__server_name=nagios_server) , ~Q(register=False)) | \
                       Q(register=False))
            elif o.__name__ is 'HostGrop':
                '''Make sure that this HostGroup instance has at least one member pointing to our destination
                nagios_server, as a nagios host_gropu may point to multiple server, and not all of them need
                to be poining to our dest server, we need to handle it in parse_to_nagios_cfg method of the
                model'''
                objs = o.objects.distinct(members__nagios_server__server_name=nagios_server)
            else:
                objs = o.objects.all()
            
            logger.debug('Found %s Objects for %s config:' % (objs.count(), o.__name__ ))
            for obj in objs:
                if o.__name__ in ('HostGroup', 'Service'):
                     '''Some Model.parse_to_nagios_cfg methods, need an extra arg.. we're telling 
                     self.export_object to pass an extra arg to it.'''
                     self.export_object(obj, os.path.join(path, 'objects'), nagios_server=nagios_server)
                else:
                    self.export_object(obj, os.path.join(path, 'objects'))
        
        self.export_object(NagiosCfg.objects.get(server_name=nagios_server), path)

    def export_object(self, nagios_obj, path , **kwargs):
        """:func:`export_object` will open a file (with the name of the object type)
        and write the content of the object to it.  """

        if not isinstance(nagios_obj, NagiosObject):
            raise RuntimeError('object received is not a NagiosObject')
        
        if not os.path.exists(path) and not path.endswith(".cfg"):
            os.mkdir(path)

        if os.path.isfile(path):
            if kwargs.get('nagios_server', None):
                self._write_file(nagios_obj.parse_to_nagios_cfg(kwargs['nagios_server']), path)
            else:
                self._write_file(nagios_obj.parse_to_nagios_cfg(), path)
        elif os.path.isdir(path):
            p = os.path.join(path, nagios_obj.FILE_NAME)
            if kwargs.get('nagios_server', None):
                self._write_file(nagios_obj.parse_to_nagios_cfg(kwargs['nagios_server'],path),p)
            else:
                self._write_file(nagios_obj.parse_to_nagios_cfg(path), p)


class Syncer(object):
    '''The Syncer automates the proces of syncronizing the config for all
    exportable nagios servers, backups its working config, checks the config and if
    it works, it will reload the nagios server, else it will rollback to the old config.
    '''

    def __init__(self, *args, **kwargs):
        self.exp = Exporter()
        self.servers=kwargs.get('server_name', False)
        logger.info('Syncer.__init__, self.servers: %s' % self.servers)
        env.use_ssh_config = True
        self.status={}
        self.bkp={}
        self.sync_log=[]
        self.output={}

    def sync(self, *args, **kwargs):
        for ns in self.get_hosts():
            logger.info('Syncer.sync, exporting %s' % ns.server_name)
            #init the action & output log for this nagios_server
            self.output[ns.server_name]=[]
            #dump local config for host.
            local_path = os.path.join(settings.STEAMER_EXP_PATH, ns.server_name)+"/"
            if not os.path.exists(local_path):
                os.mkdir(local_path)
            self.dump_local(ns.server_name, local_path)
            #remote backup of the nagios config.
            if self.rotate(ns):
                #try to reload the nagios config
                syncnreload = self.rsyncnreload(local_path, ns)
                if syncnreload is not True:
                    self.status[ns.server_name] = syncnreload
                    break
            else:
                self.sync_log.append('Could not rotate the config for %s, aborting' % ns.server_name)
                break

        return self.sync_log
    def disconnect_all(self):
        disconnect_all()

    def rsyncnreload(self, local_path, ns):

        logger.info('Syncer.rsyncnreload, called for: %s' % ns.server_name)
        with stts(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            env.host_string = ns.server_name
            rsync_out=rsync_project( ns.fabric_config_path, local_path, 
                                     [c.path for c in ns.cfg_dir.all()],
                                     True)
            self.status[ns.server_name] = False
            self.output[ns.server_name].append(rsync_out)
            self.sync_log.append('Remote synced config for %s' % ns.server_name)
            if rsync_out.succeeded:
                cfgtest_out=run('%s -v %s/nagios.cfg' % ( ns.fabric_nagios_bin, ns.fabric_config_path), pty=False)
                self.output[ns.server_name].append(rsync_out)
                if cfgtest_out.succeeded:
                    if settings.STEAMER_RESTART_NAGIOS:
                        reload_out=run('/etc/init.d/nagios restart')
                        self.output[ns.server_name].append(rsync_out)
                    self.status[ns.server_name] = True
                    self.sync_log.append('Nagios config reloaded for %s' % ns.server_name)
                else:
                    #Trying to rollback!
                    if self.rollback(ns):
                        return sync_status['ROLLBACK_MADE']
                    else:
                        return sync_status['ROLLBACK_FAILED']
            else:
                self.status[ns.server_name] = False
                self.sync_log.append('Rsync failed for %s: \n %s' % (ns.server_name, rsync_out))

            #return reload_out.succeeded or rsync_out.succeeded
            return rsync_out.succeeded

    def rotate(self, ns):
        with stts(hide('running', 'stdout', 'stderr'), warn_only=True):
            env.host_string = ns.server_name
            mkdout=run('if [ ! -d %(bkdir)s ]; then /bin/mkdir -p %(bkdir)s ;fi' % \
                    {'bkdir':ns.fabric_backups_dest})
            epoch=int(time.mktime(datetime.datetime.now().timetuple()))
            output = run('cd %(confpath)s/../ && tar cf - %(basename)s | bzip2 -9 - > \
                    %(bdest)s/djagios.%(epoch)s.tar.bz2' % \
                    {'confpath':ns.fabric_config_path, 
                     'basename':os.path.basename(ns.fabric_config_path.rstrip('/')),
                     'bdest':ns.fabric_backups_dest, 
                     'epoch':epoch})
            if output.succeeded:
                #save the last backup location, so we can roll back to the last config.
                self.bkp[ns.server_name] = '%s/djagios.%s.tar.bz2' % (ns.fabric_backups_dest, epoch)
        if mkdout.succeeded:
            self.sync_log.append('Checking for bkp location %s' % ns.fabric_backups_dest )
        if output.succeeded:
            self.sync_log.append('Remote rotated config for %s' % ns.server_name)
        else:
            self.sync_log.append('Something went wrong with %s\'s backup.' % ns.server_name)
        self.output[ns.server_name].append(output)
        return output.succeeded

    def rollback(self, ns):
        logger.info("Rollback called")
        with stts(hide('running', 'stdout', 'stderr'), warn_only=True):
            env.host_string = ns.server_name
            cmd = 'cd %(config_path)s/../  && mv %(basecfg)s %(basecfg)s.failed.%(epoch)s && \
            tar xjf %(bkpfile)s'
            out=run( cmd % {'config_path':ns.fabric_config_path, 
                            'basecfg': os.path.basename(ns.fabric_config_path.rstrip('/')),
                            'epoch':int(time.mktime(datetime.datetime.now().timetuple())),
                            'bkpfile': self.bkp[ns.server_name]})
            if out.failed:
                logger.error('Rollback failed: \n%s' % out)
            return out.succeeded

    def get_hosts(self):
        if self.servers:
            logger.info('get_hosts, self.servers: %s' % self.servers)
            return NagiosCfg.objects.filter(fabric_allow_deploy=True, server_name__in=self.servers)
        else:
            logger.info('get_hosts, self.servers: %s' % self.servers)
            return NagiosCfg.objects.filter(fabric_allow_deploy=True)

    
    def dump_local(self, server_name, directory):
        self.exp.export(directory, server_name)
        self.sync_log.append('Locally dumped config for %s at %s' % \
                (server_name, datetime.datetime.now()))

