import RPi.GPIO as gpio
from time import sleep

gpio.setwarnings(False)

button_pin = 14

gpio.setmode(gpio.BCM)
gpio.setup(button_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)

def button_callback(pin):
    print('Button pressed')

gpio.add_event_detect(button_pin, gpio.RISING, callback = button_callback)

msg = input('Press enter to quit\n\n')

gpio.cleanup()