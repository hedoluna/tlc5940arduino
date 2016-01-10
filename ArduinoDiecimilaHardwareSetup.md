## Wiring Diagram ##

![http://students.washington.edu/acleone/codes/tlc5940arduino/img/breadboard-arduino-tlc5940_close.png](http://students.washington.edu/acleone/codes/tlc5940arduino/img/breadboard-arduino-tlc5940_close.png)  ![http://tlc5940arduino.googlecode.com/files/tlc5940nt_pins.png](http://tlc5940arduino.googlecode.com/files/tlc5940nt_pins.png)

**Note: pin 1 of the Tlc is the lower right pin in the breadboard picture above.**

## Required Pins ##

  * Arduino digital pin 7 (MOSI) -> SIN (Tlc pin 26)
  * Arduino digital pin 13 (SCK) -> SCLK (Tlc pin 25)
  * Arduino digital pin 9 (OC1A) -> XLAT (Tlc pin 24)
  * Arduino digital pin 10 (OC1B) -> BLANK (Tlc pin 23)
  * Arduino digital pin 3 (OC2B) -> GSCLK (Tlc pin 18)
  * Tlc VPRG (pin 27) is at ground.  This selects between serial data going to the "greyscale" normal PWM register (VPRG=gnd) vs serial data going into the "dot-correction" register (VPRG=Vcc) (this individually adjusts the max-current through each output channel to account for differences in LED brightness).  If using the dot-correction functions in the library, this pin should be hooked to the Arduino (NOT gnd or Vcc) - see the Optional Pins section below.
  * Tlc DCPRG (pin 19) is at Vcc.  This selects between the dot-correction data in the device EEPROM (DCPRG=gnd) vs dot-correction data from the DC register in the device (DCPRG=Vcc). If using the library dot-correction functions, this should be at Vcc.

## Optional Pins ##

**VPRG** - for setting dot correction (per-channel current adjustment)
  * Arduino digital pin 8 -> VPRG (Tlc pin 27)
**XERR** - for checking for thermal overloads or disconnected LEDs
  * Arduino digital pin 12 -> XERR (Tlc pin 16)

## More Pictures ##

| ![![](http://students.washington.edu/acleone/codes/tlc5940arduino/img/breadboard-arduino-tlc5940_thumb.png)](http://students.washington.edu/acleone/codes/tlc5940arduino/img/breadboard-arduino-tlc5940.png) | ![![](http://students.washington.edu/acleone/codes/tlc5940arduino/img/breadboard-arduino-tlc5940_close_thumb.png)](http://students.washington.edu/acleone/codes/tlc5940arduino/img/breadboard-arduino-tlc5940_close.png) |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

[(SVG source)](http://students.washington.edu/acleone/codes/tlc5940arduino/img/breadboard-arduino-tlc5940.svg)