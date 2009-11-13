/*  Copyright (c) 2009 by Alex Leone <acleone ~AT~ gmail.com>

    This file is part of the Arduino TLC5940 Library.

    The Arduino TLC5940 Library is free software: you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    The Arduino TLC5940 Library is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with The Arduino TLC5940 Library.  If not, see
    <http://www.gnu.org/licenses/>. */
    
#ifndef TLC_DEFINES_H
#define TLC_DEFINES_H

/* ------------ Number of Tlc Chips Daisy Chained ---------------- */

#ifndef TLC_NUM_TLCS
#define TLC_NUM_TLCS    1
#endif

#ifndef TLC_CHANNEL_TYPE

#if TLC_NUM_TLCS < 16
#define TLC_CHANNEL_TYPE    uint8_t
#else
#define TLC_CHANNEL_TYPE    uint16_t
#endif /* -- if TLC_NUM_TLCS < 16 -- */

#endif /* -- ifndef TLC_CHANNEL_TYPE -- */


/* ------------ PWM period and timer TOP values ------------------- */

#if defined(TLC_PWM_FREQUENCY) && defined(TLC_PWM_PERIOD)
#error Can not define both TLC_PWM_FREQUENCY and TLC_PWM_PERIOD!
#endif

#ifndef TLC_PWM_FREQUENCY
#define TLC_PWM_FREQUENCY   976.5625
#endif

#ifndef TLC_PWM_PERIOD
#define TLC_PWM_PERIOD      (1.0 / (TLC_PWM_FREQUENCY))
#else
#undef  TLC_PWM_FREQUENCY
#define TLC_PWM_FREQUENCY   (1.0 / (TLC_PWM_PERIOD))
#endif /* -- ifndef TLC_PWM_PERIOD -- */

#if !(( defined(TLC_BLANK_PRESCALE) &&  defined(TLC_BLANK_TOP) \
    &&  defined(TLC_GSCLK_PRESCALE) &&  defined(TLC_GSCLK_PRESCALE)) \
   || (!defined(TLC_BLANK_PRESCALE) && !defined(TLC_BLANK_PRESCALE) \
    && !defined(TLC_GSCLK_PRESCALE) && !defined(TLC_GSCLK_PRESCALE)))
#error Define all of TLC_BLANK_PRESCALE, TLC_BLANK_TOP, TLC_GSCLK_PRESCALE, \
       and TLC_GSCLK_TOP!
#endif

#ifndef TLC_BLANK_PRESCALE
#define TLC_BLANK_PRESCALE  1
#define TLC_BLANK_TOP    (F_CPU * TLC_PWM_PERIOD / (2 * TLC_BLANK_PRESCALE))
#define TLC_GSCLK_PRESCALE  1
#define TLC_GSCLK_TOP  ((2 * TLC_GSCLK_PRESCALE * TLC_BLANK_TOP) / 4096.0 - 1)
#endif /* -- ifndef TLC_BLANK_PRESCALE -- */


/* ------------ Data Transfer Options --------------- */
#if (defined(TLC_DATA_MODE_SPI)



#endif /* -- ifdef TLC_SIN_PIN -- */


#endif /* -- ifndef TLC_DEFINES_H -- */
