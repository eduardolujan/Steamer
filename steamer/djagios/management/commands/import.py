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


from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from djagios.util import DjagiosConfigParser
import logging
import StringIO


class Command(BaseCommand):
    help = 'Imports nagios configuration to db.'

    option_list = BaseCommand.option_list + (
         make_option("-s", 
                    "--server_name", 
                    action="store", 
                    dest="server_name",
                    default='localhost',
                    help="Server name for this nagios instance."),
        make_option("-c", 
                    "--cfgfile",
                    action="store", dest="path",
                    default='nagios.cfg',
                    help="Path of the main configuration file relative to the" +\
                            " import directory."),
        make_option("-o", 
                    "--original-path",
                    action="store", dest="origpath",
                    default=None,
                    help="Path where the original main config file was without" +\
                            "the trailing file name, ej: /usr/local/nagios/etc/"),
        )
 
    def handle(self, *args, **options):
        #redirect the logger output stream to the command's stdout.
        log_handler = logging.StreamHandler(self.stdout)
        logging.root.addHandler(log_handler)
        logging.root.setLevel(logging.INFO)
        cp=DjagiosConfigParser()
        cp.load_to_db(options['path'], 
                      options['server_name'], 
                      replace=options['origpath'])
        
