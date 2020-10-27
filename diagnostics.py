# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:46:13 2020

@author: Matt
"""

import RPi.GPIO as gpio
import time
import physical_objects as ph

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

elevator = ph.Stepper(pulse = 13, direction = 19, enable = 26, steps = 8000)
dispenser = ph.Stepper(pulse = 17, direction = 27, enable = 22, steps = 800)
ultrasonic = ph.Ultrasonic(trigger = 18, echo = 21)
button = ph.Button(pin = 14)

print('Making sure everything works...')
print('Trying the candy dispenser')

ph.thread_it(dispenser)
time.sleep(3)

print('Trying the elevator. Going up...')
elevator.reverse()
ph.thread_it(elevator)
print('Going back down...')

time.sleep(2)
elevator.reverse()
elevator.steps = 9000
ph.thread_it(elevator)

print('Trying out the ultrasonic sensor...')
for i in range(10):
    dist = ultrasonic.distance()
    print('Distance measured: {} cm'.format(dist))
    time.sleep(1)
    
print('Trying out the button... press button when ready...')
ph.thread_it(button, timeout = 15)

print('Testing script finished.')