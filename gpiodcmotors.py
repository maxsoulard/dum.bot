#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import signal
import sys

class Gpiodcmotors:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(, GPIO.OUT)
        GPIO.setup(8, GPIO.OUT)
        GPIO.setup(10, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        self._reinitLedBool()

    def triggerForward(self):
        self.led10 = not self.led10
        GPIO.output(10, self.led10)

    def triggerBackward(self):
        self.led12 = not self.led12
        GPIO.output(12, self.led12)

    def triggerLeft(self):
        self.led8 = not self.led8
        GPIO.output(8, self.led8)

    def triggerRight(self):
        self.led7 = not self.led7
        GPIO.output(7, self.led7)

    def reset(self):
        self._reinitLedBool()
        GPIO.output(7, False)
        GPIO.output(10, False)
        GPIO.output(12, False)
        GPIO.output(8, False)

    def stop(self):
	self.reset()
	GPIO.cleanup()
	exit()

    def _reinitLedBool(self):
        self.led7 = False
        self.led8 = False
        self.led10 = False
        self.led12 = False

def signal_handler(signal, frame):
        GPIO.cleanup()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
