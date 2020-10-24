import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Initialize the physical objects in the system 
elevator = ph.Stepper(pulse = 13, direction = 19, enable = 26, steps = 640000, name = 'Elevator')
button = ph.Button(pin = 14)
dispenser = ph.Stepper(pulse = 17, direction = 27, enable = 22, steps = 800, name = 'Dispenser')
ultrasonic = ph.Ultrasonic(trigger = 18, echo = 10, pulse_delay = 0.00001)

# Show that each physical object is initialized
for obj in [elevator, button, dispenser, ultrasonic]:
    print(obj)

dist = 100

# The ultrasonic sensor is making some weird measurements, so let it 'warm up'
for i in range(10):
    dist = ultrasonic.distance()

try:
    while True:
        dist = ultrasonic.distance()
        
        # When the bag is in the sensor area, move the components
        if 1 < dist < 5:
            # Send the elevator up
            ph.thread_it(elevator)
            
            # Change the elevator direction and send it back down
            elevator.change_direction()
            time.sleep(0.5)
            ph.thread_it(elevator)
            
            # Get the elevator ready for the next trip
            elevator.change_direction()
            
            # Wait for the button to be pressed
            ph.thread_it(button)
            
            # Dispense candy once the button has been pressed
            ph.thread_it(dispenser)
            print('Candy dispensed')
            
        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
    print('Done')