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
Board options for the Arduino Diecimila.
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
                    {'pin': 'PB4', 'as': 'MISO', 'dir': 'i', 'unused': True},
                ),
            },
            'code': default.generator['spi_modes']['spi']['code'] \
                    .replace("DDR_SPI", "DDRB") \
                    .replace("PORT_SPI", "PORTB") \
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
                    .replace("PORT_XCK{n}", "PORTD") \
                    .replace("XCK{n}_P", "4") \
                    .replace("{n}", "0"),

        },
        
        'bitbang': default.generator['spi_modes']['bitbang'],
    },
    
    'timer_modes_order': (
        'timer1_BLANK_XLAT_timer2b_GSCLK',
        'timer1a_BLANK_timer2b_GSCLK_any_XLAT',
        'timer1b_BLANK_timer2b_GSCLK_any_XLAT',
    ),
    'timer_modes': {
        'timer1_BLANK_XLAT_timer2b_GSCLK': {
            'pins': {
                'blank': {'pin': 'PB2', 'as': 'OC1B', 'dir': 'o'},
                'xlat' : {'pin': 'PB1', 'as': 'OC1A', 'dir': 'o'},
                'gsclk': {'pin': 'PD3', 'as': 'OC2B', 'dir': 'o'},
            },
            'code': r"""
#define TLC_XLAT_INTERRUPT_vect  TIMER1_OVF_vect

#define tlc_enable_XLAT_interrupt() \
            TIFR1 |= _BV(TOV1);     \
            TIMSK1 = _BV(TOIE1)
#define tlc_disable_XLAT_interrupt() \
            TIMSK1 = 0

#define tlc_enable_XLAT_pulses() \
            TCCR1A = _BV(COM1A1) | _BV(COM1B1)
#define tlc_disable_XLAT_pulses() \
            TCCR1A = _BV(COM1B1)

inline void tlc_timers_pin_setup() {
    DDRB |= _BV(2)   // BLANK as output
          | _BV(1);  // XLAT  as output
    DDRD |= _BV(3);  // GSCLK as output
    PORTB |= _BV(2); // leave BLANK high
}

inline void tlc_timers_begin(const uint16_t div_f_osc_by) {
    TCCR1A = _BV(COM1B1);  // non inverting, output on OC1B, BLANK
    TCCR1B = _BV(WGM13);   // Phase/freq correct PWM, ICR1 top
    OCR1A = 1;             // duty factor on OC1A, XLAT is inside BLANK
    OCR1B = 2;             // duty factor on BLANK (larger than OCR1A (XLAT))
    ICR1 = 8192;
    TCCR2A = _BV(COM2B1)      // set on BOTTOM, clear on OCR2A (non-inverting),
                              // output on OC2B
           | _BV(WGM21)       // Fast pwm with OCR2A top
           | _BV(WGM20);      // Fast pwm with OCR2A top
    TCCR2B = _BV(WGM22);      // Fast pwm with OCR2A top
    OCR2B = 0;                // duty factor (as short a pulse as possible)
    OCR2A = 3;
    
    TCCR2B |= _BV(CS20);      // no prescale, (start pwm output)
    TCCR1B |= _BV(CS10);      // no prescale, (start pwm output)
}

inline void tlc_timers_pulse_xlat() {
    PORTB |=  _BV(1);
    PORTB &= ~_BV(1);
}
""",
            
        },
        
        'timer1a_BLANK_timer2b_GSCLK_any_XLAT': {
            'pins': {
                'blank': {'pin': 'PB1', 'as': 'OC1A', 'dir': 'o'},
                'xlat' : {'pin': 'any', 'as': 'TLC_XLAT_PIN', 'dir': 'o'},
                'gsclk': {'pin': 'PD3', 'as': 'OC2B', 'dir': 'o'},
            },
            'code': "",
        },
        
        'timer1b_BLANK_timer2b_GSCLK_any_XLAT': {
            'pins': {
                'blank': {'pin': 'PB2', 'as': 'OC1B', 'dir': 'o'},
                'xlat' : {'pin': 'any', 'as': 'TLC_XLAT_PIN', 'dir': 'o'},
                'gsclk': {'pin': 'PD3', 'as': 'OC2B', 'dir': 'o'},
            },
            'code': "",
        },
    },
}
