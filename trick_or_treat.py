import time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Initialize the physical objects in the system 
green_button = ph.Button(pin = 14)
yellow_button = ph.Button(pin = 26)
dispenser = ph.Stepper(pulse = 17, direction = 27, enable = 22, steps = 3200, name = 'Dispenser')
ultrasonic = ph.Ultrasonic(trigger = 18, echo = 21, pulse_delay = 0.00001, green_led = 16, red_led = 20)

# Show that each physical object is initialized
for obj in [green_button, yellow_button, dispenser, ultrasonic]:
    print(obj)

dist = 100

# Variables for logging
log_file = "halloween2020.txt"
today = time.ctime()
count = 0

ultrasonic.green_led.run()

# The ultrasonic sensor is making some weird measurements, so let it 'warm up'
for i in range(5):
    dist = ultrasonic.distance()
    time.sleep(0.2)
    
print('Happy Halloween!')

try:
    # Turn on the green light
    ultrasonic.green()
    
    # Enter the main loop
    print('Ready for the kiddos...\nPress yellow button to start')
    ph.thread_it(yellow_button)

    while True:
        dist = ultrasonic.distance()
        
        # Interrupt when the green button is pressed
        gpio.add_event_detect(green_button.pin, gpio.BOTH, callback = lambda *a: ph.thread_it(dispenser), bouncetime = 50)
        
        # When the bag is in the sensor area, move the components
        if 1 < dist < 20:
            # Turn on the red led
            ultrasonic.red()
                        
            # Dispense candy
            ph.thread_it(dispenser)
            print('Candy dispensed')
            count += 1
            
            ultrasonic.red_led.run()
            
            # Wait 4 seconds until the system can be triggered again
            time.sleep(4)
            
        time.sleep(0.2)
        ultrasonic.green()
            

except KeyboardInterrupt:
    gpio.cleanup()
    print('Done')

with open(log_file, 'a') as file:
    # Make note of the date and time
    file.write(today)
    file.write('{} kiddos served'.format(count))