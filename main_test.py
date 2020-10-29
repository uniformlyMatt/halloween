import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Initialize the physical objects in the system 
elevator = ph.Stepper(pulse = 13, direction = 19, enable = 26, steps = 55000, name = 'Elevator')
button = ph.Button(pin = 14)
dispenser = ph.Stepper(pulse = 17, direction = 27, enable = 22, steps = 3200, name = 'Dispenser')
ultrasonic = ph.Ultrasonic(trigger = 18, echo = 21, pulse_delay = 0.00001, green_led = 16, red_led = 20)

# Show that each physical object is initialized
for obj in [elevator, button, dispenser, ultrasonic]:
    print(obj)

dist = 100

ultrasonic.green_led.run()

# The ultrasonic sensor is making some weird measurements, so let it 'warm up'
for i in range(5):
    dist = ultrasonic.distance()
    time.sleep(0.2)
    
print('Happy Halloween!')

try:
    ultrasonic.green()
    while True:
        dist = ultrasonic.distance()
        
        # When the bag is in the sensor area, move the components
        if 1 < dist < 20:
            # Turn on the red led
            ultrasonic.red()
            
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
            
            ultrasonic.red_led.run()
            
            # Wait 4 seconds until the system can be triggered again
            time.sleep(4)
            
        time.sleep(0.2)
        ultrasonic.green()

except KeyboardInterrupt:
    gpio.cleanup()
    print('Done')
