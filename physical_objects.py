import time
import threading
import RPi.GPIO as gpio

class Elevator:
    def __init__(self, pulse = 23, direction = 24, enable = 25, timing_belt = 72, step_delay = 0.0000001):
        self.pulse = pulse
        self.direction = direction
        self.enable = enable
        self.timing_belt = timing_belt             # Number of steps needed to rotate the auger
        self.step_delay = step_delay   # Extremely short delay between steps
        self.pins = [pulse, direction, enable]
        
        self.ready = threading.Event()
        
        # Physical pin setup
        gpio.setup(self.pulse, gpio.OUT)
        gpio.setup(self.direction, gpio.OUT)
        gpio.setup(self.enable, gpio.OUT)
        
        # Set the direction to FORWARD
        gpio.output(self.direction, 1)
        
        # Start with the stepper motor OFF
        gpio.output(self.enable, 0)
        
    def __str__(self):
        return 'Elevator object on pins {}'.format(self.pins)
    
    def up(self):
        """ Make the elevator go up a certain length. """
        gpio.output(self.direction, 0)
        
        for i in range(self.timing_belt):
            gpio.output(self.enable, 1)
            #print('Controller enabled')

            gpio.output(self.pulse, 1)
            time.sleep(self.step_delay)
            gpio.output(self.pulse, 0)
            time.sleep(self.step_delay)

            gpio.output(self.enable, 0)
#         time.sleep(3)        
        
        return None
    
    def down(self):
        """ Make the elevator come down a certain length. """
        
        gpio.output(self.direction, 1)
        
        for i in range(self.timing_belt):
            gpio.output(self.enable, 1)
            #print('Controller enabled')

            gpio.output(self.pulse, 1)
            time.sleep(self.step_delay)
            gpio.output(self.pulse, 0)
            time.sleep(self.step_delay)

            gpio.output(self.enable, 0)
#         time.sleep(3)        
        
        return None
        
    def run(self):
        """ Make the elevator go up a certain length, then come back down. """
        self.up()
        
        # Wait 2 seconds at the top
        time.sleep(2)
        
        #self.down()
        
        self.ready.set()
        
        return 0
    
class Button:
    def __init__(self, pin = 14):
        self.pin = pin
        self.ready = threading.Event()
        
        # Set up the button pin as a physical input
        gpio.setup(self.pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)
        
    def __str__(self):
        return 'Button object on pin {}'.format(self.pin)
    
    def run(self):
        """ Wait for the button to be pressed. """
        
#         time.sleep(3)
        while True:
            if gpio.input(self.pin) == gpio.HIGH:
                self.ready.set()
                break
#         self.ready.set()
        print('\nButton pressed')
        return None
        
class Dispenser:
    def __init__(self, pulse = 17, direction = 27, enable = 22, steps = 7200, step_delay = 0.0000001):
        self.pulse = pulse
        self.direction = direction
        self.enable = enable
        self.steps = steps             # Number of steps needed to rotate the auger
        self.step_delay = step_delay   # Extremely short delay between steps
        self.pins = [pulse, direction, enable]
        
        self.ready = threading.Event()
        
        # Physical pin setup
        gpio.setup(self.pulse, gpio.OUT)
        gpio.setup(self.direction, gpio.OUT)
        gpio.setup(self.enable, gpio.OUT)
        
        # Set the direction to FORWARD
        gpio.output(self.direction, 1)
        
        # Start with the stepper motor OFF
        gpio.output(self.enable, 0)
        
    def __str__(self):
        return 'Dispenser object on pins {}'.format(self.pins)
    
    def run(self):
        """ Dispense candy """
        
        print('Rotating auger...')

        for i in range(self.steps):
            gpio.output(self.enable, 1)
            #print('Controller enabled')

            gpio.output(self.pulse, 1)
            time.sleep(self.step_delay)
            gpio.output(self.pulse, 0)
            time.sleep(self.step_delay)

            gpio.output(self.enable, 0)
#         time.sleep(3)        
        
        self.ready.set()
        print('Candy dispensed')
        
        return None
    
class Ultrasonic:
    def __init__(self, trigger = 18, echo = 10, pulse_delay = 0.00001):
        self.trigger = trigger
        self.echo = echo
        self.pulse_delay = pulse_delay
        self.pins = [trigger, echo, pulse_delay]
        
        # Physical pin setup
        gpio.setup(self.trigger, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)
        
    def __str__(self):
        return 'Ultrasonic sensor object on pins {}'.format(self.pins)
    
    def distance(self):
        """ Use the ultrasonic sensor to get a distance measurement """
        
        # Send out a pulse for 0.00001 s
        gpio.output(self.trigger, 1)
        time.sleep(self.pulse_delay)
        gpio.output(self.trigger, 0)

        start_time = time.time()
        stop_time = time.time()

        # get the time of the pulse being sent
        while gpio.input(self.echo) == 0:
            start_time = time.time()

        # get the time of the pulse returning
        while gpio.input(self.echo) == 1:
            stop_time = time.time()

        # find the round-trip time of the pulse
        elapsed_time = stop_time - start_time

        # multiply by the speed of sound (34300 cm/s)
        # and divide by 2 (there and back)
        return elapsed_time*34300/2
    
def thread_it(obj, timeout = 10):
    """ General function to handle threading for the physical components of the system. """
    
    thread = threading.Thread(target = obj.run())
    thread.start()
    
    # Run the 'run' function in the obj
    obj.ready.wait(timeout = timeout)
    
    # Clean up
    thread.join()
    obj.ready.clear()