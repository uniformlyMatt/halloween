from time import sleep, time
import RPi.GPIO as gpio

trig = 18
echo = 10

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

pulse_delay = 0.00001

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

try:
    while True:
        dist = distance()
        print('Measured distance {} cm'.format(dist))
        
        sleep(0.05)
        
except KeyboardInterrupt:
    #gpio.output(dir, 0)
        
    gpio.cleanup()
    print('Done')

