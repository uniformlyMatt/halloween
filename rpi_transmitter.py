# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:25:10 2020

@author: Matt
"""

from smbus import SMBus

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
bus.write_byte(addr, 0x1) # switch it on
input("Press return to exit")
bus.write_byte(addr, 0x0) # switch it on