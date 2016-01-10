![http://tlc5940arduino.googlecode.com/files/tlc5940nt_pins.png](http://tlc5940arduino.googlecode.com/files/tlc5940nt_pins.png)

See ArduinoDiecimilaHardwareSetup for the other pins on the Tlc that need to be connected.

## Required Pins ##

  * Mega pin 51 (MOSI) -> SIN (Tlc pin 26)
  * Mega pin 52 (SCK) -> SCLK (Tlc pin 25)
  * Mega pin 11 (OC1A) -> XLAT (Tlc pin 24)
  * Mega pin 12 (OC1B) -> BLANK (Tlc pin 23)
  * Mega pin 9 (OC2B) -> GSCLK (Tlc pin 18)

## Optional Pins ##

**VPRG** - for setting dot correction (per-channel current adjustment)
  * Mega pin 50 -> VPRG (Tlc pin 27)
**XERR** - for checking for thermal overloads or disconnected LEDs
  * Mega pin 10 -> XERR (Tlc pin 16)

## Wiring Diagram ##

Anyone want to modify the [SVG of the Arduino Diecimila](http://students.washington.edu/acleone/codes/tlc5940arduino/img/breadboard-arduino-tlc5940.svg)?