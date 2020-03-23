#!/usr/bin/python
#
# DHT11 device - Thermal & Humidity Reader for Python
#
# Run : python hdt11.py
#
# This code need Adafuruit_DHT library. Get the library with below command.
# git clone https://github.com/adafruit/Adafruit_Pyt
#


import sys
import Adafruit_DHT

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
