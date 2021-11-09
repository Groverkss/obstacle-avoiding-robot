import machine
from machine import Pin
import time

PINS = [5, 4, 14, 12]
TRIGGER_PIN = 0
ECHO_PIN = 13

int maxDist = 150;                               //Maximum sensing distance (Objects further than this distance are ignored)
int stopDist = 50;                               //Minimum distance from an object to stop in cm
float timeOut = 2*(maxDist+10)/100/340*1000000;   //Maximum time to wait for a return signal

int motorSpeed = 55;                             //The maximum motor speed
int motorOffset = 10;                             //Factor to account for one side being more powerful
int turnSpeed = 50;                               //Amount to add to motor speed when turning



class Motor:
    def __init__(self, pins):
        self.pins = [Pin(pin, Pin.OUT) for pin in pins]
        self.stop()

    def forward(self):
        self.configuration = [1, 0, 1, 0]
        self.__launch()

    def backward(self):
        self.configuration = [0, 1, 0, 1]
        self.__launch()

    def left(self):
        self.configuration = [0, 1, 1, 0]
        self.__launch()

    def right(self):
        self.configuration = [1, 0, 0, 1]
        self.__launch()

    def stop(self):
        self.configuration = [0, 0, 0, 0]
        self.__launch()

    def __launch(self):
        for i in range(4):
            self.pins[i].value(self.configuration[i])



class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """

    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=100000):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin.
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0)  # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(
                self.echo, 1, self.echo_timeout_us
            )
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110:  # 110 = ETIMEDOUT
                raise OSError("Out of range")
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms


# Led to know if NodeMCU is up
led = Pin(2, Pin.OUT)
led.off()

ultrasonic = HCSR04(TRIGGER_PIN, ECHO_PIN)
motor = Motor(PINS)
motor.forward()

def checkDirection(ultrasonic,motor):

    distances = [0,0]
    turnDir = 1

    # robot looks to the left
    motor.left()
    distances[0] = ultrasonic.distance_cm()

    # robot looks to the right
    motor.right()
    motor.right()
    distances[1] = ultrasonic.distance_cm()

    # reset robot to look forward
    motor.left()
    
    # If both directions are clear, turn left
    if (distances[0]>=200 and distances[1]>=200):
        turnDir = 0;

    # If both directions are blocked, turn around
    elif (distances[0]<=stopDist && distances[1]<=stopDist)   
        turnDir = 1;
    # If left has more space, turn left
    elif (distances[0]>=distances[1])                          
        turnDir = 0;
    # If right has more space, turn right
    elif (distances[0]<distances[1])                           
        turnDir = 2;
  
    return turnDir;


while True:

    time.sleep(0.75)
    
    distance = ultrasonic.distance_cm()

    if(distance >= stopDist): motor.forward()

    while(distance >= stopDist):
        distance = ultrasonic.distance_cm()
        time.sleep(0.25)
    
    motor.stop()

    turnDir = checkDirection(ultrasonic,motor)
    print(turnDir)

    if(turnDir == 0):
        motor.left()
    
    elif(turnDir == 1):
        motor.left()
        motor.left()
    
    elif(turnDir == 2):
        motor.right()
    
