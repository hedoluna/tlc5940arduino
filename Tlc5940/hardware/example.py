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
To make the library work with a new board or mcu:
1. Copy this file and fill in the info.
2. Run generate.py
3. tlc_{filename}.h will be generated and tlc_board_select.h will be updated.
4. Send me (acleone ~AT~ gmail.com) the .py file so I can put it in the library.


Include Logic - How the library decides which board file to include:
1. If any defines match any of the 'board_macros', eg.
     #define __MY_SPIFFY_DEV_BOARD__
     #include "Tlc5940.h"
2. If the mcu matches any of the 'mcu_macros'.  If multiple boards use the
   same mcu, see mcu_order.py
3. Throw an error.
"""

import default

generator = {

    # If any of these are defined, force the library to use this board include.
    'board_macros': ('__MY_SPIFFY_DEV_BOARD__'),

    # Which mcu(s) this board uses.
    # See http://www.nongnu.org/avr-libc/user-manual/using_tools.html
    # for the list of mcu macros.
    # Note: if more than one board uses the same mcu, See mcu_order.py
    'mcu_macros': ('__AVR_ATmega168__', '__AVR_ATmega168P__'),
    
    # SPI modes.  Order is best first.
    'spi_modes_order': ('spi', 'usart0', 'bitbang'),
    'spi_modes': {
        'spi': {
            'pins': { # for automagically generating pin-outs
                'sin' : {'pin': 'PB3', 'as': 'MOSI', 'dir': 'o'},
                'sclk': {'pin': 'PB5', 'as': 'SCK',  'dir': 'o'},
                'others': (
                    # SS has to be set as output or the SPI module will switch
                    # to slave if the pin goes low
                    {'pin': 'PB2', 'as': 'SS', 'dir': 'o', 'unused': True},
                ),
            },
            
            'code': """
void tlc_spi_begin() {
    ...
}

void tlc_spi_write(const uint8_t byte) {
    ...
}
""",

        },
        'usart0': {
            'pins': {
                'sin' : {'pin': 'PD1', 'as': 'TXD0', 'dir': 'o'},
                'sclk': {'pin': 'PD4', 'as': 'XCK0', 'dir': 'o'},
            },
            
            'code': """
void tlc_spi_begin() {
    ...
}

void tlc_spi_write(const uint8_t byte) {
    ...
}
""",

        },
        'bitbang': default.generator['spi_modes']['bitbang'],
    },
    
    
}
