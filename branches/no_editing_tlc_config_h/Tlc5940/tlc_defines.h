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
    
#if !defined(TLC_DEFINES_H)
#    define  TLC_DEFINES_H

/* ------------ Number of Tlc Chips Daisy Chained ---------------- */

#if !defined(NUM_TLCS)
#  define NUM_TLCS    1
#endif

#if !defined(TLC_CHANNEL_TYPE)
#  if NUM_TLCS < 16
#    define TLC_CHANNEL_TYPE    uint8_t
#  else
#    define TLC_CHANNEL_TYPE    uint16_t
#  endif
#endif /* !defined(TLC_CHANNEL_TYPE) */

#endif /* !defined(TLC_DEFINES_H) */
