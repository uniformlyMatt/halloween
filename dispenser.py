# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 11:29:57 2020

@author: Matt
"""

import RPi.GPIO as GPIO          
from time import sleep

button_pin = 21

motor_in1 = 24
motor_in2 = 23
en = 25
temp1 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN)

GPIO.output(motor_in1, GPIO.LOW)
GPIO.output(motor_in2, GPIO.LOW)

candy = GPIO.input(button_pin)

p = GPIO.PWM(en,1000)
p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

while(True):

    x = raw_input()
    
    if x=='r':
        print("run")
        if temp1:
         GPIO.output(motor_in1,GPIO.HIGH)
         GPIO.output(motor_in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(motor_in1,GPIO.LOW)
         GPIO.output(motor_in2,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(motor_in1,GPIO.LOW)
        GPIO.output(motor_in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(motor_in1,GPIO.HIGH)
        GPIO.output(motor_in2,GPIO.LOW)
        temp1 = 1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(motor_in1,GPIO.LOW)
        GPIO.output(motor_in2,GPIO.HIGH)
        temp1 = 0
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        x='z'
        
    elif candy:
        print("forward")
        GPIO.output(motor_in1, GPIO.HIGH)
        GPIO.output(motor_in2, GPIO.LOW)
        templ = 1
        x = 'z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")