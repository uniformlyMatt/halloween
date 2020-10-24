import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

dispenser = ph.Stepper(pulse = 17, direction = 27, enable = 22, steps = 800, name = 'Dispenser')

print(dispenser)

# Run the test

# Push the candy out
ph.thread_it(dispenser)

print('Done')