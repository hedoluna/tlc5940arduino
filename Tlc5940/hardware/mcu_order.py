# Copyright (c) 2009 by Alex Leone <acleone ~AT~ gmail.com>
#
# This file is part of the Arduino TLC5940 Library.
#
# The Arduino TLC5940 Library is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# The Arduino TLC5940 Library is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with The Arduino TLC5940 Library.  If not, see
# <http://www.gnu.org/licenses/>.

"""
This file defines the which board gets included if only an mcu macro is
defined and two boards use the same mcu.

For example, if two boards both have '__AVR_ATmega168__' in 'mcu_macros',
then the board file listed below will get the include.
"""

mcu_order = {
}
