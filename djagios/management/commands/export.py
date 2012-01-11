import logging 
import StringIO

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from steamer.djagios.util import Syncer


class Command(BaseCommand):
    args = 'path'
    help = 'Exports nagios configuration to db.'

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
        sync = Syncer(server_name=options['server_name'].split(","))
        sync.sync()
        self.stdout.write("%s\n\n" % "\n".join(sync.sync_log)) 
        self.stdout.write("%s" % sync.output) 
