import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Initialize the physical objects in the system 
elevator = ph.Elevator(pulse = 13, direction = 19, enable = 26, timing_belt = 640000)
button = ph.Button(pin = 14)
dispenser = ph.Dispenser(pulse = 17, direction = 27, enable = 22)
ultrasonic = ph.Ultrasonic(trigger = 18, echo = 10, pulse_delay = 0.00001)

dist = 100

try:
    while True:
##        ph.thread_it(button)
        ph.thread_it(dispenser)
        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
    print('Done')