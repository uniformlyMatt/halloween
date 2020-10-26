import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

elevator = ph.Stepper(pulse = 13, direction = 19, enable = 26, steps = 56000, name = 'Elevator')

print(elevator)

# Run the test

# Send the elevator up
#elevator.reverse()
ph.thread_it(elevator)
##print(elevator.fwd)
time.sleep(0.5)

# Change the elevator direction and send it back down

print(elevator.bwd)
#elevator.reverse()
##time.sleep(0.5)
#ph.thread_it(elevator)

gpio.cleanup()
print('Done')
