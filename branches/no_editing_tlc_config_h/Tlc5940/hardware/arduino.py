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
Board options for the Arduino Diecimila
"""

import default

generator = {

    # If any of these are defined, force the library to use this board include.
    'board_macros': (),

    # Which mcu(s) this board uses.
    # See http://www.nongnu.org/avr-libc/user-manual/using_tools.html
    # for the list of mcu macros.
    # Note: if more than one board uses the same mcu, See mcu_order.py
    'mcu_macros': ('__AVR_ATmega48__', '__AVR_ATmega48P__',
                   '__AVR_ATmega88__', '__AVR_ATmega88P__',
                   '__AVR_ATmega168__', '__AVR_ATmega168P__',
                   '__AVR_ATmega328P__'),
    
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
            'code': default.generator['spi_modes']['spi']['code'] \
                    .replace("DDR_SPI", "DDRB") \
                    .replace("MOSI_P", "3") \
                    .replace("SCK_P", "5") \
                    .replace("SS_P", "2"),

        },
        
        'usart0': {
            'pins': {
                'sin' : {'pin': 'PD1', 'as': 'TXD0', 'dir': 'o'},
                'sclk': {'pin': 'PD4', 'as': 'XCK0', 'dir': 'o'},
            },       
            'code': default.generator['spi_modes']['usart{n}']['code'] \
                    .replace("DDR_XCK{n}", "DDRD") \
                    .replace("XCK{n}_P", "4") \
                    .replace("{n}", "0"),

        },
        
        'bitbang': default.generator['spi_modes']['bitbang'],
    },
    
    'timer_modes_order': (
        'timer1_BLANK_timer2b_GSCLK',
    ),
    'timer_modes': {
        'timer1_BLANK_timer2b_GSCLK': {
            'pins': {
                'blank': {'pin': 'PB2', 'as': 'OC1B', 'dir': 'o'},
                'xlat' : {'pin': 'PB1', 'as': 'OC1A', 'dir': 'o'},
                'gsclk': {'pin': 'PD3', 'as': 'OC2B', 'dir': 'o'},
            },
            
        },
        
        'timer2_BLANK_timer1_GSCLK': {
        
        },
    },
}
