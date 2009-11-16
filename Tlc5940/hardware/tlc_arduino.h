#if !defined(TLC_ARDUINO_H)
#    define  TLC_ARDUINO_H

#if defined(TLC_SPI_MODE_SPI) \
      + defined(TLC_SPI_MODE_USART0) \
      + defined(TLC_SPI_MODE_BITBANG) > 1
#  error at most 1 mode can be defined of: ['TLC_SPI_MODE_SPI', 'TLC_SPI_MODE_USART0', 'TLC_SPI_MODE_BITBANG']
#elif defined(TLC_SPI_MODE_SPI) \
      + defined(TLC_SPI_MODE_USART0) \
      + defined(TLC_SPI_MODE_BITBANG) == 0
#  define TLC_SPI_MODE_SPI
#endif

#if defined(TLC_SPI_MODE_SPI)

inline void tlc_spi_begin() {
    DDRB |= _BV(3) // MOSI as output
          | _BV(5)  // SCK as output
          | _BV(2);  // SS as output
    SPSR = _BV(SPI2X); // set speed to f_osc / 2
    SPCR = _BV(SPE)    // enable SPI
         | _BV(MSTR);  // in master mode
}

inline void tlc_spi_write(const uint8_t byte) {
    SPDR = byte; // starts transmission
    while ( !(SPSR & _BV(SPIF)) )
        ; // wait for transmission complete
}

inline void tlc_spi_pulse_sclk() {
    PORTB |= _BV(5);
    PORTB &= ~_BV(5);
}

#endif /* defined(TLC_SPI_MODE_SPI) */


#if defined(TLC_SPI_MODE_USART0)

inline void tlc_spi_begin() {
    DDRD |= _BV(4); // XCK0 as output, enables master mode
    UCSR0C = _BV(UMSEL01) | _BV(UMSEL00); // USART0 in master SPI mode
    UCSR0B = _BV(TXEN0); // TXD0 as output
    UBRR0 = 0; // set speed to f_osc / 2 (has to be set after TXD0 enabled)
}

inline void tlc_spi_write(const uint8_t byte) {
    UDR0 = byte;
    while ( !(UCSR0A & _BV(UDRE0)) )
        ; // wait for transmit buffer to be empty
}

inline void tlc_spi_pulse_sclk() {
    PORTD |= _BV(4);
    PORTD &= ~_BV(4);
}

#endif /* defined(TLC_SPI_MODE_USART0) */


#if defined(TLC_SPI_MODE_BITBANG)

#if defined(TLC_SIN_PIN) + defined(TLC_SCLK_PIN) != 2
#  error TLC_SIN_PIN and TLC_SCLK_PIN must be defined with TLC_SPI_MODE_BITBANG!
#endif

inline void tlc_spi_begin() {
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
        PORT_HIGH(TLC_SCLK_PIN);
        PORT_LOW(TLC_SCLK_PIN);
    }
}

inline void tlc_spi_pulse_sclk() {
    PORT_HIGH(TLC_SCLK_PIN);
    PORT_LOW(TLC_SCLK_PIN);
}

#endif /* defined(TLC_SPI_MODE_BITBANG) */


#if defined(TLC_TIMER_MODE_TIMER1_BLANK_XLAT_TIMER2B_GSCLK) \
      + defined(TLC_TIMER_MODE_TIMER1A_BLANK_TIMER2B_GSCLK_ANY_XLAT) \
      + defined(TLC_TIMER_MODE_TIMER1B_BLANK_TIMER2B_GSCLK_ANY_XLAT) > 1
#  error at most 1 mode can be defined of: ['TLC_TIMER_MODE_TIMER1_BLANK_XLAT_TIMER2B_GSCLK', 'TLC_TIMER_MODE_TIMER1A_BLANK_TIMER2B_GSCLK_ANY_XLAT', 'TLC_TIMER_MODE_TIMER1B_BLANK_TIMER2B_GSCLK_ANY_XLAT']
#elif defined(TLC_TIMER_MODE_TIMER1_BLANK_XLAT_TIMER2B_GSCLK) \
      + defined(TLC_TIMER_MODE_TIMER1A_BLANK_TIMER2B_GSCLK_ANY_XLAT) \
      + defined(TLC_TIMER_MODE_TIMER1B_BLANK_TIMER2B_GSCLK_ANY_XLAT) == 0
#  define TLC_TIMER_MODE_TIMER1_BLANK_XLAT_TIMER2B_GSCLK
#endif

#if defined(TLC_TIMER_MODE_TIMER1_BLANK_XLAT_TIMER2B_GSCLK)

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

#endif /* defined(TLC_TIMER_MODE_TIMER1_BLANK_XLAT_TIMER2B_GSCLK) */


#if defined(TLC_TIMER_MODE_TIMER1A_BLANK_TIMER2B_GSCLK_ANY_XLAT)

#endif /* defined(TLC_TIMER_MODE_TIMER1A_BLANK_TIMER2B_GSCLK_ANY_XLAT) */


#if defined(TLC_TIMER_MODE_TIMER1B_BLANK_TIMER2B_GSCLK_ANY_XLAT)

#endif /* defined(TLC_TIMER_MODE_TIMER1B_BLANK_TIMER2B_GSCLK_ANY_XLAT) */


#endif /* !defined(TLC_ARDUINO_H) */

