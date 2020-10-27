import time
import threading
import RPi.GPIO as gpio

class Stepper:
    def __init__(self, pulse = 23, direction = 24, enable = 25, steps = 80, step_delay = 0.0000001, name = 'Elevator'):
        self.pulse = pulse
        self.direction = direction
        self.enable = enable
        self.steps = steps             # Number of steps to move the Stepper
        self.set_steps = steps         # Permanent number of steps
        self.step_delay = step_delay   # Extremely short delay between steps
        self.name = name
        self.pins = [pulse, direction, enable]
        
        self.ready = threading.Event()
        
        # Physical pin setup
        gpio.setup(self.pulse, gpio.OUT)
        gpio.setup(self.direction, gpio.OUT)
        gpio.setup(self.enable, gpio.OUT)
        
        # Set the direction to FORWARD
        gpio.output(self.direction, 1)
        self.bwd = True
##        print('{} direction set to FWD'.format(self.name))
        
        # Start with the stepper motor OFF
        gpio.output(self.enable, 0)
        
    def __str__(self):
        return 'Stepper object {} on pins {}'.format(self.name, self.pins)
    
    def reset_elevator(self):
        """ Function to put the Elevator in its ready position """
        
        if self.name == 'Elevator':
            self.bwd = True
            self.steps = 8000
            
            self.run()
            
            self.steps = self.set_steps
                
        else:
            return None
    
    def reverse(self):
        """ Switch direction. """
        
        if self.bwd:
            self.bwd = False
            print('Direction set to FWD')
        elif not self.bwd:
            self.bwd = True
            print('Direction set to BWD')
            
        return None
        
    def run(self):
        """ Make the Stepper run for a set number of steps """
        
        if self.bwd:
            gpio.output(self.direction, 1)
        else:
            gpio.output(self.direction, 0)
        
        gpio.output(self.enable, 1)
        for step in range(self.steps):
            gpio.output(self.pulse, 1)
            time.sleep(self.step_delay)
            gpio.output(self.pulse, 0)
            time.sleep(self.step_delay)

        gpio.output(self.enable, 0)
        self.ready.set()
        
        return None
    
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
        
        while True:
            if gpio.input(self.pin) == gpio.HIGH:
                self.ready.set()
                break

        print('\nButton pressed')
        return None
    
class Ultrasonic:
    def __init__(self, trigger = 18, echo = 21, pulse_delay = 0.00001):
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
    
class LED:
    def __init__(self, pin = 5, blinks = 10):
        self.pin = pin
        
        # Physical pin setup
        gpio.setup(self.pin, gpio.OUT)
        gpio.output(self.pin, 0)
        
    def __str__(self):
        return "LED object on pin {}".format(self.pin)
        
    def on(self):
        """ Simply turn the LED on """
        
        gpio.output(self.pin, 1)
        
        return None
    
    def off(self):
        """ Simply turn the LED off """
        
        gpio.output(self.pin, 0)
        
    def blink(self):
        """ Make the LED blink a set amount of blinks """
        
        for i in range(self.blinks):
            # Turn the LED on
            self.on()
            
            time.sleep(0.05)
            
            # Turn the LED off
            self.off()
        
        return None
    
    def run(self):
        """ Blink the LED. I had to do it this way to use threading. """
        pass
    
def thread_it(obj, timeout = 10):
    """ General function to handle threading for the physical components of the system. """
    
    thread = threading.Thread(target = obj.run())
    thread.start()
    
    # Run the 'run' function in the obj
    obj.ready.wait(timeout = timeout)
    
    # Clean up
    thread.join()
    obj.ready.clear()
    
    return None