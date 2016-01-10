# Introduction #

The [Brilldea LED Painter Kit](http://www.brilldea.com/product_LEDPainter.html) has 3 tlc's, as "Red" (channels 0 - 15), "Green" (channels 16-31), "Blue" (channels 32-47).

![http://tlc5940arduino.googlecode.com/files/brilldea_LP_controls_wtext.png](http://tlc5940arduino.googlecode.com/files/brilldea_LP_controls_wtext.png)

## Hardware Setup for the Arduino Diecimila/Duemilanove ##
### Required Pins ###

  * Arduino digital pin 7 (MOSI) -> SIN-RED (J3  pin 5)
  * Arduino digital pin 13 (SCK) -> SCLK (J3 pin 4)
  * Arduino digital pin 9 (OC1A) -> XLAT (J3 pin 3)
  * Arduino digital pin 10 (OC1B) -> BLANK (J3 pin 8)
  * Arduino digital pin 3 (OC2B) -> GSCLK (J3 pin 7)
  * VPRG (J3 pin 10) should be hooked to gnd, or if using the dot-correction functions, the Arduino (see Optional Pins below).
  * DCPRG (J3 pin 9) Vcc (5V).

### Optional Pins ###

**VPRG** - for setting dot correction (per-channel current adjustment)
  * Arduino digital pin 8 -> VPRG (J3 pin 10)