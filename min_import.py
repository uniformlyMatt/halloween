# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:45:02 2020

@author: Matt
"""

import RPi.GPIO as gpio
import time
import physical_objects as ph

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)