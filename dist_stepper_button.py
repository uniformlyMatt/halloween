from time import sleep, time
import RPi.GPIO as gpio
import physical_objects as ph

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Initialize the physical objects in the system 
elevator = ph.Elevator(motor1 = 23, motor2 = 24, enable = 25, speed = 50)
button = ph.Button(pin = 14)
dispenser = ph.Dispenser(pulse = 17, direction = 27, enable = 22)
ultrasonic = ph.Ultrasonic(trigger = 18, echo = 10, pulse_delay = 0.00001)
   
try:
    while True:
        dist = ultrasonic.distance()
        
        if dist > 5:
            print('\nDistance measurements stopped at {} cm'.format(dist))
            ph.thread_it(elevator)
            ph.thread_it(button)
            ph.thread_it(dispenser)
            
            print('All done, back to measuring distance...')

except KeyboardInterrupt:
    gpio.output(dir, 0)
    gpio.cleanup()
    print('Done')
