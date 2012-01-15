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

from string import letters
from string import digits
from string import punctuation
from random import choice

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Generates a new SECRET_KEY."
    requires_model_validation = False
    can_import_settings = True

    def handle_noargs(self, **options):
        ch = letters + digits + punctuation
        return ''.join([choice(ch) for i in range(50)])+"\n"
