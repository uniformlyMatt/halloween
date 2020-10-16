import RPi.GPIO as gpio
import time

out_pin = 14

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(out_pin, gpio.OUT)

gpio.output(out_pin, 0)

for i in range(20):
    gpio.output(out_pin, 1)
    time.sleep(2)