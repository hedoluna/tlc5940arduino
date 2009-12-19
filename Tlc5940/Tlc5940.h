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

#if !defined(TLC5940_H)
#    define  TLC5940_H

#include <avr/io.h>
#include <avr/interrupt.h>
#include <inttypes.h>

#include "tlc_defines.h"
#include "hardware/tlc_board_select.h"
/* hardware will define:
   Defines:
    - TLC_XLAT_INTERRUPT_vect
   Macros:
    - tlc_enable_XLAT_interrupt()
    - tlc_disable_XLAT_interrupt()
    - tlc_enable_XLAT_pulses()
    - tlc_disable_XLAT_pulses()
   Functions:
    - void tlc_spi_begin()
    - void tlc_spi_write(const uint8_t byte)
    - void tlc_spi_pulse_sclk()
    - void tlc_timers_pin_setup()
    - void tlc_timers_begin(const uint16_t div_f_osc_by)
    - void tlc_timers_pulse_xlat()
*/


/** The main Tlc5940 class for the entire library.  An instance of this class
    will be preinstantiated as Tlc. */
class Tlc5940
{
  public:
    void begin(uint16_t initialValue = 0, uint16_t div_f_osc_by = 2);
    void clear(void);
    uint8_t update(void);
    void set(TLC_CHANNEL_TYPE channel, uint16_t value);
    uint16_t get(TLC_CHANNEL_TYPE channel);
    void setAll(uint16_t value);
#if defined(VPRG_ENABLED)
    void setAllDC(uint8_t value);
#endif
#if defined(XERR_ENABLED)
    uint8_t readXERR(void);
#endif

};

#if defined(VPRG_ENABLED)
void tlc_dcModeStart(void);
void tlc_dcModeStop(void);
#endif




/** This will be true (!= 0) if update was just called and the data has not
    been latched in yet. */
volatile uint8_t tlc_needXLAT;

/** Some of the extened library will need to be called after a successful
    update. */
volatile void (*tlc_onUpdateFinished)(void);

/** Packed grayscale data, 24 bytes (16 * 12 bits) per TLC.

    Format: Lets assume we have 2 TLCs, A and B, daisy-chained with the SOUT of
    A going into the SIN of B.
    - byte 0: upper 8 bits of B.15
    - byte 1: lower 4 bits of B.15 and upper 4 bits of B.14
    - byte 2: lower 8 bits of B.0
    - ...
    - byte 24: upper 8 bits of A.15
    - byte 25: lower 4 bits of A.15 and upper 4 bits of A.14
    - ...
    - byte 47: lower 8 bits of A.0

    \note Normally packing data like this is bad practice.  But in this
          situation, shifting the data out is really fast because the format of
          the array is the same as the format of the TLC's serial interface. */
uint8_t tlc_GSData[NUM_TLCS * 24];

#if defined(VPRG_ENABLED)
/** Don't add an extra SCLK pulse after switching from dot-correction mode. */
uint8_t tlc_firstGSInput;
#endif

/** Interrupt called after an XLAT pulse to prevent more XLAT pulses. */
ISR(TLC_XLAT_INTERRUPT_vect) {
    tlc_disable_XLAT_pulses();
    tlc_disable_XLAT_interrupt();
    tlc_needXLAT = 0;
    if (tlc_onUpdateFinished) {
        sei();
        tlc_onUpdateFinished();
    }
}

/** \defgroup ReqVPRG_ENABLED Functions that Require VPRG_ENABLED
    Functions that require VPRG_ENABLED == 1.
    You can enable VPRG by changing
    \code #define VPRG_ENABLED    0 \endcode to
    \code #define VPRG_ENABLED    1 \endcode in tlc_config.h

    You will also have to connect Arduino digital pin 6 to TLC pin 27. (The
    pin to be used can be changed in tlc_config.h).  If VPRG is not enabled,
    the TLC pin should grounded (remember to unconnect TLC pin 27 from GND
    if you do enable VPRG). */
/* @{ */ /* @} */

/** \defgroup CoreFunctions Core Libary Functions
    These function are all prefixed with "Tlc." */
/* @{ */

/** Pin i/o and Timer setup.  The grayscale register will be reset to all
    zeros, or whatever initialValue is set to and the Timers will start.
    \param initialValue = 0, optional parameter specifing the inital startup
           value */
void Tlc5940::begin(uint16_t initialValue, uint16_t div_f_osc_by) {
#if defined(VPRG_ENABLED)
    VPRG_DDR |= _BV(VPRG_PIN);
    VPRG_PORT &= ~_BV(VPRG_PIN);  // grayscale mode (VPRG low)
#endif
#if defined(XERR_ENABLED)
    XERR_DDR &= ~_BV(XERR_PIN);   // XERR as input
    XERR_PORT |= _BV(XERR_PIN);   // enable pull-up resistor
#endif
    tlc_spi_begin();
    tlc_timers_pin_setup();
    setAll(initialValue);
    update();
    tlc_disable_XLAT_pulses();
    tlc_disable_XLAT_interrupt();
    tlc_needXLAT = 0;
    tlc_timers_pulse_xlat();
    tlc_timers_begin(div_f_osc_by);
    update();
}

/** Sets the grayscale data array, #tlc_GSData, to all zeros, but does not
    shift in any data.  This call should be followed by update() if you are
    turning off all the outputs. */
void Tlc5940::clear(void) {
    setAll(0);
}

/** Shifts in the data from the grayscale data array, #tlc_GSData.
    If data has already been shifted in this grayscale cycle, another call to
    update() will immediately return 1 without shifting in the new data.  To
    ensure that a call to update() does shift in new data, use
    \code while(Tlc.update()); \endcode
    or
    \code while(tlc_needXLAT); \endcode
    \returns 1 if there is data waiting to be latched, 0 if data was
             successfully shifted in */
uint8_t Tlc5940::update(void) {
    if (tlc_needXLAT) {
        return 1;
    }
    tlc_disable_XLAT_pulses();
#if defined(VPRG_ENABLED)
    if (tlc_firstGSInput) {
        // adds an extra SCLK pulse unless we've just set dot-correction data
        tlc_firstGSInput = 0;
    } else {
        tlc_spi_pulse_sclk();
    }
#else
    tlc_spi_pulse_sclk();
#endif
    uint8_t *p = tlc_GSData;
    while (p < tlc_GSData + NUM_TLCS * 24) {
        tlc_spi_write(*p++);
        tlc_spi_write(*p++);
        tlc_spi_write(*p++);
    }
    tlc_needXLAT = 1;
    tlc_enable_XLAT_pulses();
    tlc_enable_XLAT_interrupt();
    return 0;
}

/** Sets channel to value in the grayscale data array, #tlc_GSData.
    \param channel (0 to #NUM_TLCS * 16 - 1).  OUT0 of the first TLC is
           channel 0, OUT0 of the next TLC is channel 16, etc.
    \param value (0-4095).  The grayscale value, 4095 is maximum.
    \see get */
void Tlc5940::set(TLC_CHANNEL_TYPE channel, uint16_t value) {
    TLC_CHANNEL_TYPE index8 = (NUM_TLCS * 16 - 1) - channel;
    uint8_t *index12p = tlc_GSData + ((((uint16_t)index8) * 3) >> 1);
    if (index8 & 1) { // starts in the middle
                      // first 4 bits intact | 4 top bits of value
        *index12p = (*index12p & 0xF0) | (value >> 8);
                      // 8 lower bits of value
        *(++index12p) = value & 0xFF;
    } else { // starts clean
                      // 8 upper bits of value
        *(index12p++) = value >> 4;
                      // 4 lower bits of value | last 4 bits intact
        *index12p = ((uint8_t)(value << 4)) | (*index12p & 0xF);
    }
}

/** Gets the current grayscale value for a channel
    \param channel (0 to #NUM_TLCS * 16 - 1).  OUT0 of the first TLC is
           channel 0, OUT0 of the next TLC is channel 16, etc.
    \returns current grayscale value (0 - 4095) for channel
    \see set */
uint16_t Tlc5940::get(TLC_CHANNEL_TYPE channel) {
    TLC_CHANNEL_TYPE index8 = (NUM_TLCS * 16 - 1) - channel;
    uint8_t *index12p = tlc_GSData + ((((uint16_t)index8) * 3) >> 1);
    return (index8 & 1)? // starts in the middle
            (((uint16_t)(*index12p & 15)) << 8) | // upper 4 bits
            *(index12p + 1)                       // lower 8 bits
        : // starts clean
            (((uint16_t)(*index12p)) << 4) | // upper 8 bits
            ((*(index12p + 1) & 0xF0) >> 4); // lower 4 bits
}

/** Sets all channels to value.
    \param value grayscale value (0 - 4095) */
void Tlc5940::setAll(uint16_t value) {
    uint8_t firstByte = value >> 4;
    uint8_t secondByte = (value << 4) | (value >> 8);
    uint8_t *p = tlc_GSData;
    while (p < tlc_GSData + NUM_TLCS * 24) {
        *p++ = firstByte;
        *p++ = secondByte;
        *p++ = (uint8_t)value;
    }
}

#if defined(VPRG_ENABLED)

/** \addtogroup ReqVPRG_ENABLED
    From the \ref CoreFunctions "Core Functions":
    - \link Tlc5940::setAllDC Tlc.setAllDC(uint8_t value(0-63)) \endlink - sets
      all the dot correction data to value */
/* @{ */

/** Sets the dot correction for all channels to value.  The dot correction
    value correspondes to maximum output current by
    \f$\displaystyle I_{OUT_n} = I_{max} \times \frac{DCn}{63} \f$
    where
    - \f$\displaystyle I_{max} = \frac{1.24V}{R_{IREF}} \times 31.5 =
         \frac{39.06}{R_{IREF}} \f$
    - DCn is the dot correction value for channel n
    \param value (0-63) */
void Tlc5940::setAllDC(uint8_t value) {
    tlc_dcModeStart();

    uint8_t firstByte = value << 2 | value >> 4;
    uint8_t secondByte = value << 4 | value >> 2;
    uint8_t thirdByte = value << 6 | value;

    for (TLC_CHANNEL_TYPE i = 0; i < NUM_TLCS * 12; i += 3) {
        tlc_spi_write(firstByte);
        tlc_spi_write(secondByte);
        tlc_spi_write(thirdByte);
    }
    tlc_timers_pulse_xlat();

    tlc_dcModeStop();
}

/* @} */

#endif

#if defined(XERR_ENABLED)

/** Checks for shorted/broken LEDs reported by any of the TLCs.
    \returns 1 if a TLC is reporting an error, 0 otherwise. */
uint8_t Tlc5940::readXERR(void) {
    return ((XERR_PINS & _BV(XERR_PIN)) == 0);
}

#endif

/* @} */

#if defined(VPRG_ENABLED)

/** Switches to dot correction mode and clears any waiting grayscale latches.*/
void tlc_dcModeStart(void)
{
    tlc_disable_XLAT_pulses(); // ensure that no latches happen
    tlc_disable_XLAT_interrupt(); // (in case this was called right after update)
    tlc_needXLAT = 0;
    VPRG_PORT |= _BV(VPRG_PIN); // dot correction mode
}

/** Switches back to grayscale mode. */
void tlc_dcModeStop(void)
{
    VPRG_PORT &= ~_BV(VPRG_PIN); // back to grayscale mode
    tlc_firstGSInput = 1;
}

#endif

/** Preinstantiated Tlc variable. */
Tlc5940 Tlc;


#endif /* !defined(TLC5940_H) */
