from string import letters, digits, punctuation
from random import choice

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Generates a new SECRET_KEY."
    requires_model_validation = False
    can_import_settings = True

    def handle_noargs(self, **options):
        return ''.join([choice(letters + digits + punctuation) for i in range(50)])+"\n"
