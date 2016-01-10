![http://tlc5940arduino.googlecode.com/files/tlc5940nt_pins.png](http://tlc5940arduino.googlecode.com/files/tlc5940nt_pins.png)

See ArduinoDiecimilaHardwareSetup for the other pins on the Tlc that need to be connected.

## Required Pins ##

  * Sanguino pin 5 (MOSI) -> SIN (Tlc pin 26)
  * Sanguino pin 7 (SCK) -> SCLK (Tlc pin 25)
  * Sanguino pin 13 (OC1A) -> XLAT (Tlc pin 24)
  * Sanguino pin 12 (OC1B) -> BLANK (Tlc pin 23)
  * Sanguino pin 14 (OC2B) -> GSCLK (Tlc pin 18)

## Optional Pins ##

**VPRG** - for setting dot correction (per-channel current adjustment)
  * Sanguino pin 15 -> VPRG (Tlc pin 27)
**XERR** - for checking for thermal overloads or disconnected LEDs
  * Sanguino pin 6 -> XERR (Tlc pin 16)

## Wiring Diagram ##

Anyone want to modify the [SVG of the Arduino Diecimila](http://students.washington.edu/acleone/codes/tlc5940arduino/img/breadboard-arduino-tlc5940.svg)?