from time import sleep
import RPi.GPIO as gpio

pul = 17
dir = 27
ena = 22

#diri = 14
#enai = 15
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(pul, gpio.OUT)
gpio.setup(dir, gpio.OUT)
gpio.setup(ena, gpio.OUT)
#gpio.setup(enai, gpio.OUT)

gpio.output(dir, 1)

#gpio.output(enai, 1)

duration_fwd = 5000

delay = 0.0000001
print('Between-step delay set to {} '.format(delay))

cycles = 1000
cyclecount = 0

def forward():
    gpio.output(ena, gpio.HIGH)
    #gpio.output(enai, gpio.HIGH)
    #print('Controller enabled')
    
    
    gpio.output(pul, gpio.HIGH)
    sleep(delay)
    gpio.output(pul, gpio.LOW)
    sleep(delay)
        
    gpio.output(ena, gpio.LOW)
    #gpio.output(enai, gpio.LOW)
    return 0

for i in range(2400):
    forward()

gpio.output(dir, 0)
    
gpio.cleanup()
print('Done')