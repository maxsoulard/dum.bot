# dum.bot

Small two wheels robot controlled through a webapp or autonomous with ultrasonic sensor. 

<img src="http://letsmakerobots.com/files/userpics/u23549/2015-03-12_17_46_29.jpg" />

<img src="http://i.imgur.com/LmgWtXQ.gif" />
<img src="http://i.imgur.com/i0YkQDE.gif" />


<b>Parts</b>

<ul>
<li>Raspberry pi B</li>
<li>Pi camera</li>
<li>Adafruit Trinket</li>
<li>HC-SR04</li>
<li>Pololu Zumo chassis kit with 4xAA to power the motors and the Trinket</li>
<li>Micro metal gearmotor HP 75:1</li>
<li>L298N breakout board</li>
<li>USB battery pack 5000mAh (to power the Pi)</li>
<li>2x servo motor tower pro SG90 (yet to implement)</li>
<li>USB WiFi dongle</li>
<li>Some resistances, breadboards and wires</li>
</ul>

<b>Software</b>

Majority of source code is in python. For the webapp, CherryPy is used (minimalist web framework) and some Javascript (jQuery) for client side code : ajax requests are sent to activate wanted motors (Pi’s GPIO set to HIGH). A second ajax request is sent when the key or touch screen is released to set the Pi’s GPIO to LOW. It stops the activated motors.

RPi.GPIO to control motors via pi’s gpio. For turning right and left functions, I had to use à time.sleep because there was too much lag to have a precise control on turning functions. Now I just turn for 100 m, no matter how long the key is pressed.

Mjpeg-streamer was used for Pi camera streaming (tutos found online). There is a slight lag but it is all devices compatible without any codecs (it is basically an img tag which is constantly refreshed).

Adafruit_I2C library to get datas from the Adafruit Trinket which control the HC-SR04 via I2C.

Arduino code is pretty simple. I will add a servomotor soon but the Trinket has no hardware PWM implementation, so maybe I’ll replace it by a Arduino Nano like.

A simple algorithm to avoid detected obstacle thanks to datas sent by the Trinket. Basically, if an obstacle is closer than 10 centimeters, dum.bot goes back for 200 ms then turn left. If another obstacle is detected, it tries left again. If the way is still not clear, it turns right to check it out. To have a more precise value for obstacle range, it reads 5 values, then removes the min and max values and calculate the average from the 3 left.

<b>TODO</b>

<ul>
<li>Add servo on HC-SR04</li>
<li>Replace Trinket by Nano</li>
<li>Correct or remove pi camera servos control</li>
<li>Complete install.sh script</li>
<li>Add infrared LED</li>
<li>Add void sensor on the front</li>
</ul>
