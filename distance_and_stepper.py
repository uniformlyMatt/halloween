from time import sleep, time
import RPi.GPIO as gpio

pul = 17
dir = 27
ena = 22

button_pin = 14

trig = 18
echo = 24

diri = 14
enai = 15
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(pul, gpio.OUT)
gpio.setup(dir, gpio.OUT)
gpio.setup(ena, gpio.OUT)
gpio.setup(enai, gpio.OUT)

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
gpio.setup(button_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)

gpio.output(dir, 1)

duration_fwd = 5000

pulse_delay = 0.00001
step_delay = 0.0000001
print('Between-step delay set to {} '.format(step_delay))

def distance():
    # Send out a pulse for 0.00001 s
    gpio.output(trig, 1)
    sleep(pulse_delay)
    gpio.output(trig, 0)
    
    start_time = time()
    stop_time = time()
    
    # get the time of the pulse being sent
    while gpio.input(echo) == 0:
        start_time = time()
        
    # get the time of the pulse returning
    while gpio.input(echo) == 1:
        stop_time = time()
        
    # find the round-trip time of the pulse
    elapsed_time = stop_time - start_time
    
    # multiply by the speed of sound (34300 cm/s)
    # and divide by 2 (there and back)
    
    return elapsed_time*34300/2
    
def forward():
    gpio.output(ena, gpio.HIGH)
    gpio.output(enai, gpio.HIGH)
    #print('Controller enabled')
    
    gpio.output(pul, gpio.HIGH)
    sleep(step_delay)
    gpio.output(pul, gpio.LOW)
    sleep(step_delay)
        
    gpio.output(ena, gpio.LOW)
    gpio.output(enai, gpio.LOW)
    return None

try:
    while True:
        dist = distance()
        print('Measured distance {} cm'.format(dist))
        
        sleep(0.05)
        
        if gpio.input(button_pin) == gpio.HIGH:
            for i in range(2400):
                forward()
except KeyboardInterrupt:
    gpio.output(dir, 0)
        
    gpio.cleanup()
    print('Done')
