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

class ParseError(Exception):
    """Exception should be rased when parsing to or from the nagios format failed"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Error occured got error message: %s"%self.msg

class InvalidObjectError(Exception):
    """Exception should be rased when deserializing from an external stream"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Error occured got error message: %s"%self.msg
