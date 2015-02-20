import RPi.GPIO as GPIO
import time
from utils import *


class Gpioservo():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(21, GPIO.OUT)
        self.p = GPIO.PWM(21,50)
        self.p.start(7.5)
        self.angle = 90
        self.direction = ''

    def turnCam(self):
        try:
            if self.direction == 'left' and self.angle < 180:
                self.angle += 45
                self._servoRun()
            elif self.direction == 'right' and self.angle > 0:
                self.angle -= 45
                self._servoRun()

        except KeyboardInterrupt:
            self.p.ChangeDutyCycle(7.5)
            self.p.stop()
            GPIO.cleanup()

    def _servoRun(self):
        dc = Utils.angletodutycycle(self.angle)
        self.p.ChangeDutyCycle(dc)
        time.sleep(1)

    def setDirection(self, direction):
        self.direction = direction

    def getDirection(self):
        return self.direction
