import time
import wiringpi2 as wiringpi
from threading import Thread
from utils import *
from constantes import *


class Gpioservo(Thread):
    def __init__(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(Constantes.SERVO1PIN,2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetClock(400)
        wiringpi.pwmSetRange(1024)
        try:
            wiringpi.pwmWrite(Constantes.SERVO1PIN, 0)
        except Exception as e:
            print str(e)
        self.angle = 90
        self.direction = ''
        self.dtMin, self.dtMax = 35, 120
        self.dt = self.dtMax
        wiringpi.pwmWrite(Constantes.SERVO1PIN, self.dt)

    def run(self):
        try:
            if self.direction == Constantes.CAMLEFT:
                print "CAM LEFT"
                dtemp = self.dt + 10
                if dtemp > self.dtMax:
                    self.dt = self.dtMax
                else:
                    self.dt = dtemp
                wiringpi.pwmWrite(Constantes.SERVO1PIN, self.dt)
                print "DT = "+str(self.dt)

            elif self.direction == Constantes.CAMRIGHT:
                print "CAM RIGHT"
                dtemp = self.dt - 10
                if dtemp < self.dtMin:
                    self.dt = self.dtMin
                else:
                    self.dt = dtemp
                wiringpi.pwmWrite(Constantes.SERVO1PIN, self.dt)
                print "DT = "+str(self.dt)

            time.sleep(0.2)
        except Exception as e:
            # clean up
            wiringpi.pwmWrite(Constantes.SERVO1PIN, 0)
            print("exiting.")
            print(str(e))

    def setDirection(self, direction):
        self.direction = direction

    def getDirection(self):
        return self.direction
