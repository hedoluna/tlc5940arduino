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
The default generator.  Import this module if you want to use it as some of the
options in another generator:

import default
default_bb = default.generator['spi_modes']['bitbang']
"""

generator = {
    'board_macros': (),
    'mcu_macros': (),
    'spi_modes_order': ('spi', 'usart{n}', 'bitbang'),
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
inline void tlc_spi_begin() {
    DDR_SPI |= _BV(MOSI_P) // MOSI as output
          | _BV(SCK_P)  // SCK as output
          | _BV(SS_P);  // SS as output
    SPSR = _BV(SPI2X); // set speed to f_osc / 2
    SPCR = _BV(SPE)    // enable SPI
         | _BV(MSTR);  // in master mode
}

inline void tlc_spi_write(const uint8_t byte) {
    SPDR = byte; // starts transmission
    while ( !(SPSR & _BV(SPIF)) )
        ; // wait for transmission complete
}
""",

        },
        'usart{n}': {
            'pins': {
                'sin' : {'pin': 'PD1', 'as': 'TXD{n}', 'dir': 'o'},
                'sclk': {'pin': 'PD4', 'as': 'XCK{n}', 'dir': 'o'},
            },
            
            'code': """
inline void tlc_spi_begin() {
    DDR_XCK{n} |= _BV(XCK{n}_P); // XCK{n} as output, enables master mode
    UCSR{n}C = _BV(UMSEL{n}1) | _BV(UMSEL{n}0); // USART{n} in master SPI mode
    UCSR{n}B = _BV(TXEN{n}); // TXD{n} as output
    UBRR0 = 0; // set speed to f_osc / 2 (has to be set after TXD{n} enabled)
}

inline void tlc_spi_write(const uint8_t byte) {
    UDR{n} = byte;
    while ( !(UCSR{n}A & _BV(UDRE{n})) )
        ; // wait for transmit buffer to be empty
}
""",

        },
        'bitbang': {
            'pins': {
                'sin' : {'pin': 'any', 'as': 'TLC_SIN_PIN',  'dir': 'o'},
                'sclk': {'pin': 'any', 'as': 'TLC_SCLK_PIN', 'dir': 'o'},
            },
            'code':
"""
#if defined(TLC_SIN_PIN) + defined(TLC_SCLK_PIN) != 2
#  error TLC_SIN_PIN and TLC_SCLK_PIN must be defined with TLC_SPI_MODE_BITBANG!
#endif

void tlc_spi_begin() {
    DDR_HIGH(TLC_SIN_PIN);
    DDR_HIGH(TLC_SCLK_PIN);
}

void tlc_spi_write(const uint8_t byte) {
    uint8_t bit = 0x80;
    for (; bit; bit >>= 1) {
        if (bit & byte) {
            PORT_HIGH(TLC_SIN_PIN);
        } else {
            PORT_LOW(TLC_SIN_PIN);
        }
        PORT_HIGH(TLC_SIN_PIN);
        PORT_LOW(TLC_SIN_PIN);
    }
}
""",            
        },
    },    
}

