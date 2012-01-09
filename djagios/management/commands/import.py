from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from djagios.util import DjagiosConfigParser
import logging
import StringIO


class Command(BaseCommand):
    args = 'path'
    help = 'Imports nagios configuration to db.'

    option_list = BaseCommand.option_list + (
         make_option("-s", 
                    "--server_name", 
                    action="store", 
                    dest="server_name",
                    default='localhost',
                    help="Submit the server name for the config"),
        make_option("-p", 
                    "--path",
                    action="store", dest="path",
                    default='/etc/nagios/nagios.cfg',
                    help="Path of the main configuration file."),
        )
 
    def handle(self, *args, **options):
        log_handler = logging.StreamHandler(self.stdout)
        logging.root.addHandler(log_handler)
        logging.root.setLevel(logging.INFO)
        cp=DjagiosConfigParser()
        cp.load_to_db(options['path'], options['server_name'])
        
