import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Initialize the physical objects in the system 
elevator = ph.Stepper(pulse = 13, direction = 19, enable = 26, steps = 54000, name = 'Elevator')
button = ph.Button(pin = 14)
dispenser = ph.Stepper(pulse = 17, direction = 27, enable = 22, steps = 800, name = 'Dispenser')
ultrasonic = ph.Ultrasonic(trigger = 18, echo = 21, pulse_delay = 0.00001)

# Show that each physical object is initialized
for obj in [elevator, button, dispenser, ultrasonic]:
    print(obj)

dist = 100

# The ultrasonic sensor is making some weird measurements, so let it 'warm up'
for i in range(5):
    dist = ultrasonic.distance()
    time.sleep(0.2)

try:
    while True:
        dist = ultrasonic.distance()
        
        # When the bag is in the sensor area, move the components
        if 1 < dist < 20:
            # Send the elevator up
            
            elevator.reverse()
            ph.thread_it(elevator)
            
            # Get the elevator ready for the next trip
            time.sleep(2)

            elevator.reverse()
            ph.thread_it(elevator)
            
            # Wait for the button to be pressed
            ph.thread_it(button)
            
            # Dispense candy once the button has been pressed
            ph.thread_it(dispenser)
            print('Candy dispensed')
            
            # Wait 5 seconds until the system can be triggered again
            time.sleep(5)
            
        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
    print('Done')