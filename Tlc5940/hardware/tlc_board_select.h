#if !defined(TLC_BOARD_SELECT_H)
#    define  TLC_BOARD_SELECT_H

#if defined(__AVR_ATmega48__)  \
 || defined(__AVR_ATmega168P__)  \
 || defined(__AVR_ATmega328P__)  \
 || defined(__AVR_ATmega88__)  \
 || defined(__AVR_ATmega48P__)  \
 || defined(__AVR_ATmega88P__)  \
 || defined(__AVR_ATmega168__)
#  include "tlc_arduino.h"
#else
#  error Board not recognized! Please send an email to acleone ~AT~ gmail.com to add support for your board.
#endif

#endif /* !defined(TLC_BOARD_SELECT_H) */

