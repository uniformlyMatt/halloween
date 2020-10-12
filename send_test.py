# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:49:48 2020

@author: Matt

Make sure you put a 220 Ohm resistor in series between the RPi and Arduino

"""

import RPi.GPIO as gpio
import time

arduino_pin = 27

gpio.setmode(gpio.BCM)
gpio.setup(arduino_pin, gpio.OUT)

gpio.output(arduino_pin, 0)

while True:
    command = raw_input()
    
    if command == 's':
        gpio.output(arduino_pin, 1)
        time.sleep(0.5)
        command = 'z'
        
    elif command == 'e':
        print('Exit')
        gpio.cleanup()
        break
    
    else:
        print('Wrong input. The options are:\n"s" - send output\n"e" - exit')
    