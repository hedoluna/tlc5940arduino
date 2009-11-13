#if !defined(TLC_ARDUINO_H)
#    define  TLC_ARDUINO_H

#if defined(TLC_SPI_MODE_SPI) + defined(TLC_SPI_MODE_USART0) + defined(TLC_SPI_MODE_BITBANG) > 1
#  error at most 1 spi mode can be defined: ['TLC_SPI_MODE_SPI', 'TLC_SPI_MODE_USART0', 'TLC_SPI_MODE_BITBANG']
#elif defined(TLC_SPI_MODE_SPI) + defined(TLC_SPI_MODE_USART0) + defined(TLC_SPI_MODE_BITBANG) == 0
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

#endif /* defined(TLC_SPI_MODE_USART0) */


#if defined(TLC_SPI_MODE_BITBANG)

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

#endif /* defined(TLC_SPI_MODE_BITBANG) */


#endif /* !defined(TLC_ARDUINO_H) */

