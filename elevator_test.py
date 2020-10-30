import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

elevator = ph.Stepper(pulse = 13, direction = 19, enable = 26, steps = 56000, name = 'Elevator')

print(elevator)

# Run the test

# Send the elevator up
print("Going up")
elevator.reverse()
ph.thread_it(elevator)

time.sleep(3)

# Change the elevator direction and send it back down

print("Coming back down")
elevator.reverse()
ph.thread_it(elevator)

gpio.cleanup()
print('Done')
