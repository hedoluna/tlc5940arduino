An Arduino Library for the Texas Instruments TLC5940 16-channel LED Driver.  Mailing list: https://groups.google.com/forum/?fromgroups#!forum/tlc5940arduino

### Installation and Examples ###
Unzip the Tlc5940\_xxx.zip folder into the arduino/libraries/ folder.

Then look at the BasicUse example (File -> Examples -> Tlc5940 -> BasicUse).

### News ###

  * Now supports the Teensy board.  Also check out http://www.pjrc.com/teensy/td_libs_Tlc5940.html for videos of some of the example sketches.

  * Multiplexing (still alpha): [Tlc5940Mux\_2.zip](http://tlc5940arduino.googlecode.com/files/Tlc5940Mux_2.zip).  Also see http://www.youtube.com/watch?v=U1t9usUr9ns - 3 tlc's drive the entire 8x11 grid, by driving one row at a time and switching through the rows.  This is the Serial example in Tlc5940Mux.  [The circuitry](http://tlc5940arduino.googlecode.com/svn/trunk/Tlc5940Mux/tlc5940mux_circuit_example.png).

  * Now supports servos! See the example (Sketchbook->Examples->Library-Tlc5940->Servos) and [documentation](http://alex.kathack.com/codes/tlc5940arduino/html_r014/tlc__servos_8h.html).

### Code Documentation ###
Online documentation generated from Doxygen is available at
http://alex.kathack.com/codes/tlc5940arduino/html_r014/

Check the mailing list at https://groups.google.com/forum/?fromgroups#!forum/tlc5940arduino

### Hardware Setup ###

  * Arduino Diecimila & Duemilanove: ArduinoDiecimilaHardwareSetup
  * Arduino Mega: ArduinoMegaHardwareSetup
  * Arduino Pro Micro: ArduinoProMicroHardwareSetup
  * Teensy: http://www.pjrc.com/teensy/td_libs_Tlc5940.html
  * Sanguino: SanguinoHardwareSetup
  * Brilldea LED Painter: [BrilldeaLEDPainter](http://code.google.com/p/tlc5940arduino/wiki/BrilldeaLEDPainter)

Also read PowerDissipation

| ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/breadboard-arduino-tlc5940_thumb.png)](http://tlc5940arduino.googlecode.com/svn/wiki/images/breadboard-arduino-tlc5940.png) | ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/breadboard-arduino-tlc5940_close_thumb.png)](http://tlc5940arduino.googlecode.com/svn/wiki/images/breadboard-arduino-tlc5940_close.png) |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

[(SVG source)](http://tlc5940arduino.googlecode.com/svn/wiki/images/breadboard-arduino-tlc5940.svg)

## Some Projects ##

### Tlc5940Mux Serial Example ###

http://www.youtube.com/watch?v=U1t9usUr9ns

| ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/rocks_nopaper_150.jpg)](http://tlc5940arduino.googlecode.com/svn/wiki/images/rocks_nopaper.jpg) | ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/my_nopaper_150.jpg)](http://tlc5940arduino.googlecode.com/svn/wiki/images/my_nopaper.jpg) | ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/tlc5940mux_circuit_example_150.png)](http://tlc5940arduino.googlecode.com/svn/trunk/Tlc5940Mux/tlc5940mux_circuit_example.png) |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

[(KiCad .sch file)](http://tlc5940arduino.googlecode.com/svn/trunk/Tlc5940Mux/tlc5940mux_circuit_example.sch)

### Persistence of Vision with 1 tlc ###

| ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0416_150.jpg)](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0416_950.jpg) | ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0468_150.jpg)](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0468_950.jpg) |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------|

The Basic Animations example from the library

### Persistence of Vision with 3 tlc's for color ###

| ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0655_150.jpg)](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0655_950.jpg) | ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0662_150.jpg)](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0662_950.jpg) | ![![](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0663_150.jpg)](http://tlc5940arduino.googlecode.com/svn/wiki/images/IMG_0663_950.jpg) |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------|

A first very uncalibrated attempt

## Questions? ##

Check the mailing list: https://groups.google.com/forum/?fromgroups#!forum/tlc5940arduino