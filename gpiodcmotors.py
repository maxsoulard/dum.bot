#!/usr/bin/env python

import RPi.GPIO as GPIO
import time


class Gpio:
    def __init__(self, pin):
        self.pin = pin
        self.status = False
        GPIO.setup(self.pin, GPIO.OUT)

    def output(self, bool):
        self.status = bool
        GPIO.output(self.pin, self.status)


class Gpiodcmotors:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.gpio7 = Gpio(7)
        self.gpio8 = Gpio(8)
        self.gpio10 = Gpio(10)
        self.gpio16 = Gpio(16)
        GPIO.setwarnings(False)
        self.reset()

    def triggerForward(self):
        self.gpio10.output(not self.gpio10.status)
        self.gpio7.output(not self.gpio7.status)

    def triggerBackward(self):
        self.gpio8.output(not self.gpio8.status)
        self.gpio16.output(not self.gpio16.status)

    def triggerRight(self):
        self.gpio8.output(not self.gpio8.status)
        self.gpio10.output(not self.gpio10.status)
        time.sleep(0.1)
        self.gpio8.output(not self.gpio8.status)
        self.gpio10.output(not self.gpio10.status)


    def triggerLeft(self):
        self.gpio7.output(not self.gpio7.status)
        self.gpio16.output(not self.gpio16.status)
        time.sleep(0.1)
        self.gpio7.output(not self.gpio7.status)
        self.gpio16.output(not self.gpio16.status)

    def reset(self):
        self.gpio7.output(False)
        self.gpio8.output(False)
        self.gpio10.output(False)
        self.gpio16.output(False)

    def stop(self):
        # self.reset()
        GPIO.cleanup()
        exit()
