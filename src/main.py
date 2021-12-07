import machine
from machine import Pin
import time
import network

import urequests
import ujson

PINS = [5, 4, 14, 12]
TRIGGER_PIN = 0
ECHO_PIN = 13

# Minimum distance from an object to stop in cm
stopDist = 25

TURN_TIME = 800  # ms

# onem2m server
uri_cnt = "https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-11/Node-1/Data"

WIFI_SSID = "Archer C6"
WIFI_PASS = "Kunwar@123"

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
        time.sleep_ms(TURN_TIME)

    def right(self):
        self.configuration = [1, 0, 0, 1]
        self.__launch()
        time.sleep_ms(TURN_TIME)

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


ultrasonic = HCSR04(TRIGGER_PIN, ECHO_PIN)
motor = Motor(PINS)
motor.forward()

def create_data_cin(uri_cnt, value, cin_labels="", data_format="json"):
    """
    Method description:
    Deletes/Unregisters an application entity(AE) from the OneM2M framework/tree
    under the specified CSE

    Parameters:
    uri_cse : [str] URI of parent CSE
    ae_name : [str] name of the AE
    fmt_ex : [str] payload format
    """
    headers = {
        "X-M2M-Origin": "2vCsok51z6:xB2p5Mj@N2",
        "Content-type": "application/{};ty=4".format(data_format),
    }

    body = {
        "m2m:cin": {"con": "{}".format(value), "lbl": cin_labels, "cnf": "text"}
    }

    response = urequests.post(uri_cnt, data=ujson.dumps(body), headers=headers)
    print("Return code : {}".format(response.status_code))
    print("Return Content : {}".format(response.text))

def get_data(uri, data_format="json"):
    """
        Method description:
        Deletes/Unregisters an application entity(AE) from the OneM2M framework/tree
        under the specified CSE

        Parameters:
        uri_cse : [str] URI of parent CSE
        ae_name : [str] name of the AE
        fmt_ex : [str] payload format
    """
    headers = {
        'X-M2M-Origin': '2vCsok51z6:xB2p5Mj@N2',
        'Content-type': 'application/{}'.format(data_format)}

    response = requests.get(uri, headers=headers)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    _resp = json.loads(response.text)
    return response.status_code, _resp["m2m:cin"]["con"] ## To get latest or oldest content instance
    # return response.status_code, _resp["m2m:cnt"]#["con"] ## to get whole data of container (all content instances)

def checkDirection(ultrasonic, motor):

    distances = [0, 0]
    turnDir = 1

    # robot looks to the left
    print("Going to look left")
    motor.left()
    distances[0] = ultrasonic.distance_cm()

    print("Distance at left: ", distances[0])

    # robot looks to the right
    print("Going to look right")
    motor.right()
    motor.right()
    distances[1] = ultrasonic.distance_cm()

    print("Distance at right: ", distances[1])

    # reset robot to look forward
    motor.left()

    # If both directions are clear, turn left
    if distances[0] >= 200 and distances[1] >= 200:
        turnDir = 0

    # If both directions are blocked, turn around
    elif distances[0] <= stopDist and distances[1] <= stopDist:
        turnDir = 1
    # If left has more space, turn left
    elif distances[0] >= distances[1]:
        turnDir = 0
    # If right has more space, turn right
    elif distances[0] < distances[1]:
        turnDir = 2

    return turnDir


def start():

    # delete datacontainer directions
    # delete(str.concat(uri_cnt,"Directions"), data_format="json")

    # create datacontainer directions
    # create_cnt(str.concat(uri_cnt,"Directions"),cnt_labels=["Directions"], data_format="json")

    # Led to know if NodeMCU is up
    led = Pin(2, Pin.OUT)
    led.off()

    print("Starting!")
    motor.forward()

    while True:

        start = get_data(
            uri_cnt + "/State"
            )

        if start == "stop": 
            motor.stop()
            continue

        time.sleep(0.75)

        distance = ultrasonic.distance_cm()

        if distance >= stopDist:
            motor.forward()

        while distance >= stopDist:
            distance = ultrasonic.distance_cm()

        motor.stop()

        turnDir = checkDirection(ultrasonic, motor)

        if turnDir == 0:
            motor.left()
            # adding no of obstacles
            print("Turn Left")
            # create_data_cin(
            #     uri_cnt + "/Directions",
            #     "Left",
            #     cin_labels=["Left"],
            # )

        elif turnDir == 1:
            motor.left()
            motor.left()
            print("Turn Around")
            # adding no of obstacles
            # create_data_cin(
            #     uri_cnt + "/Directions",
            #     "180",
            #     cin_labels=["Turned around"],
            # )

        elif turnDir == 2:
            motor.right()
            print("Turn Right")
            # adding no of obstacles
            # create_data_cin(
            #     uri_cnt + "/Directions",
            #     "Right",
            #     cin_labels=["Right"],
            # )


if __name__ == "__main__":

    # Connect to wifi
    # sta_if = network.WLAN(network.STA_IF)
    # sta_if.active(True)
    # sta_if.connect(WIFI_SSID, WIFI_PASS)
    # print("IFCONFIG:")
    # print(sta_if.ifconfig())

    start()
    # create_data_cin(str.concat(uri_cnt,"/Directions"), "Left", cin_labels=["Left"], data_format="json")
    # create_data_cin(str.concat(uri_cnt,"/Directions"), "180", cin_labels=["Turned around"], data_format="json")
    # create_data_cin(str.concat(uri_cnt,"/Directions"), "Right", cin_labels=["Right"], data_format="json")
