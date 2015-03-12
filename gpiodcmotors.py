#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import signal
import sys

class Gpiodcmotors:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(8, GPIO.OUT)
        GPIO.setup(10, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setwarnings(False)
        self._reinitgpiobool()

    def triggerForward(self):
        self.gpio10 = not self.gpio10
        GPIO.output(10, self.gpio10)
        self.gpio7 = not self.gpio7
        GPIO.output(7, self.gpio7)
        GPIO.output(11, self.gpio7)
        GPIO.output(13, self.gpio7)

    def triggerBackward(self):
        self.gpio16 = not self.gpio16
        GPIO.output(16, self.gpio16)
        self.gpio8 = not self.gpio8
        GPIO.output(8, self.gpio8)
        GPIO.output(11, self.gpio8)
        GPIO.output(13, self.gpio8)

    def triggerRight(self):
        self.gpio8 = not self.gpio8
        GPIO.output(8, self.gpio8)
        self.gpio10 = not self.gpio10
        GPIO.output(10, self.gpio10)
        GPIO.output(13, self.gpio10)

    def triggerLeft(self):
        self.gpio7 = not self.gpio7
        GPIO.output(7, self.gpio7)
        self.gpio16 = not self.gpio16
        GPIO.output(16, self.gpio16)
        GPIO.output(11, self.gpio16)

    def reset(self):
        self._reinitgpiobool()
        GPIO.output(7, False)
        GPIO.output(10, False)
        GPIO.output(16, False)
        GPIO.output(8, False)
        GPIO.output(11, False)

    def stop(self):
        # self.reset()
        GPIO.cleanup()
        exit()

    def _reinitgpiobool(self):
        self.gpio7 = False
        self.gpio8 = False
        self.gpio10 = False
        self.gpio16 = False
