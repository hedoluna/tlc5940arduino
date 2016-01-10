![http://tlc5940arduino.googlecode.com/files/tlc5940nt_pins.png](http://tlc5940arduino.googlecode.com/files/tlc5940nt_pins.png)

See ArduinoDiecimilaHardwareSetup for the other pins on the Tlc that need to be connected.

## Required Pins ##

http://www.sparkfun.com/products/10998
  * MOSI (Pro micro D16) -> SIN (TLC pin 26)
  * SCK (Pro micro D15) -> SCLK (TLC pin 25)
  * SS (Pro micro D14 - not necessary to hook up, just don't use as an input)
  * OC1A (Pro micro D9) -> XLAT (TLC pin 24)
  * OC1B (Pro micro D10) -> BLANK (TLC pin 23)
  * OC3A (Pro micro D5) -> GSCLK (TLC pin 18)

http://www.sparkfun.com/products/11098
  * MOSI (Pro micro D16) -> SIN (TLC pin 26)
  * SCK (Pro micro D15) -> SCLK (TLC pin 25)
  * SS (Pro micro D17/RX LED - not necessary to hook up, just don't use as input.  Note that this pin doesn't actually have a solder hole so don't worry about it)
  * OC1A (Pro micro D9) -> XLAT (TLC pin 24)
  * OC1B (Pro micro D10) -> BLANK (TLC pin 23)
  * OC3A (Pro micro D5) -> GSCLK (TLC pin 18)