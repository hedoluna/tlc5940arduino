# Power Dissipation #

From the datasheet:

![http://tlc5940arduino.googlecode.com/files/power_dissipation_eq.png](http://tlc5940arduino.googlecode.com/files/power_dissipation_eq.png)

## Explanation ##

  * V<sub>cc</sub> is +5V for regular Arduino's.
  * I<sub>cc</sub> (Supply current) is listed in Electrical Characteristics on pg 4 of the datasheet: <br> <img src='http://tlc5940arduino.googlecode.com/files/icc_table.png' /> <br> I'll assume you're using R_iref = ~2k, so I<sub>cc</sub> < 25mA. (Data transfer is usually 8MHz, and assuming outputs are on).<br>
<ul><li>V<sub>out</sub> is the voltage going into the tlc pin, which would be the voltage going into the LED minus the forward voltage drop across the LED.  For example, +4V --> LED --> TLC, then Vout = 4 - (forward voltage drop across LED, usually 2.1V, see the LED datasheet) = 1.9V.  I'll assume you're using +5V, so +5V - 2.1V = 2.9V.<br>
</li><li>I<sub>max</sub> is the calculated from the R<sub>iref</sub> resistor, I<sub>max</sub> = 39.06 / R<sub>iref</sub>.  I'll assume R<sub>iref</sub> = 2k so I<sub>max</sub> = 39.06 / 2000 = 20mA.<br>
</li><li>DCn is the dot correction value for channel n.  Unless you're setting the dot correction, it's 63.<br>
</li><li>d<sub>pwm</sub> is the current channel setting, (aka GS PWM value), divided by 4095.  For example, <code>Tlc.set(0, 4095)</code> means d<sub>pwm</sub> = 4095/4095 = 1.  Lets assume d<sub>pwm</sub> = 1.<br>
</li><li>N is the number of channels set to d<sub>pwm</sub>.  For example, if we know that we're not going to turn on more than 5 channels at once, then N = 5.  Lets assume N = 16, or we might turn all channels on at some point.</li></ul>

<h2>Example Calculation</h2>

Here's our assumptions from above:<br>
<ul><li>V<sub>cc</sub> = 5V<br>
</li><li>I<sub>cc</sub> < 25mA (Looking up value with R<sub>iref</sub> = 2k from table above)<br>
</li><li>V<sub>out</sub> = 2.9V (assuming +5V --> LED with Vf of 2.1V --> TLC)<br>
</li><li>I<sub>max</sub> = 39.06 / R<sub>iref</sub> = 20mA.  (Assuming R<sub>iref</sub> = 2k)<br>
</li><li>DC<sub>n</sub> = 63 (unless you explicitly set this)<br>
</li><li>d<sub>pwm</sub> = 1 (whatever the maximum channel setting will be, eg <code>Tlc.set(0, 4095)</code> -> 4095/4095 = 1)<br>
</li><li>N = 16 (maximum number of channels that will be on at once)</li></ul>

P<sub>d</sub> = (V<sub>cc</sub> <code>*</code> I<sub>cc</sub>) + (V<sub>out</sub> <code>*</code> I<sub>max</sub> <code>*</code> (DC<sub>n</sub> / 63) <code>*</code> d<sub>pwm</sub> <code>*</code> N)<br>
<br> = (5V <code>*</code> 25mA) + (2.9V <code>*</code> 20mA <code>*</code> (63 / 63 = 1) <code>*</code> 1 <code>*</code> 16) = 1053mW<br>
<br>
<img src='http://tlc5940arduino.googlecode.com/files/dissipation_ratings.png' />

Let's assume that the chip is in an environment with a ambient temperature T<sub>a</sub> = 30C.  Then by power dissipation table (DIP is the package that fits on a breadboard), the maximum power dissipation is 2456mW - 19.65mW <code>*</code> (T<sub>a</sub> - 25C = 30C - 25C = 5) = 2357.75mW.<br>
<br>
So from before, if R<sub>iref</sub> = 2k, the LED voltage is 5V, and all the outputs are on, the chip generates 1053mW and we should be fine.<br>
<br>
Now assume that we lowered the LED voltage to 4V (so +4V --> LED --> TLC).  Then <br>
Pd = (5V <code>*</code> 25mA) + (1.9V <code>*</code> 20mA <code>*</code> (63 / 63 = 1) <code>*</code> 1 <code>*</code> 16) = 733mW<br>
<br>
So if you're afraid of burning out TLCs, lower the LED voltage.  But make sure it's enough voltage to turn on the LEDs! It should be a bit above the forward voltage drop from the LED datasheet.