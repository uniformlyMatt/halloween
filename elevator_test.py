import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Initialize the elevator 
elevator = ph.Elevator(motor1 = 23, motor2 = 24, enable = 25, speed = 65)
    
try:
    while True:    
        ph.thread_it(elevator)

except KeyboardInterrupt:
    gpio.cleanup()
    print('Done')