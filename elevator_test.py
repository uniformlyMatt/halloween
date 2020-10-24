import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

elevator = ph.Stepper(pulse = 13, direction = 19, enable = 26, steps = 57600, name = 'Elevator')

print(elevator)

# Run the test

# Send the elevator up
ph.thread_it(elevator)

# Change the elevator direction and send it back down
elevator.change_direction()
time.sleep(0.5)
ph.thread_it(elevator)

# Get the elevator ready for the next trip
elevator.change_direction()
print('Done')