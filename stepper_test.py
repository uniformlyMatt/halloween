from time import sleep
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

elevator = ph.Stepper(pulse = 13, direction = 19, enable = 26, steps = 57600)

print(elevator)