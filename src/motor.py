import machine
from machine import Pin
import time

PINS = [5, 4, 14, 12]


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


led = Pin(2, Pin.OUT)
led.off()

motor = Motor(PINS)
motor.left()
time.sleep(100)
