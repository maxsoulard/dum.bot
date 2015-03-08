import time
import wiringpi2 as wiringpi
from threading import Thread
from utils import *
from constantes import *

class Servo():
    def __init__(self):
        self.angle = 90
        self.direction = ''
        self.dtMin, self.dtMax = 35, 120
        self.dt = 65
    def setDirection(self, direction):
        self.direction = direction

    def getDirection(self):
        return self.direction


class Gpioservo():
    def __init__(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(Constantes.SERVO1PIN,2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetClock(400)
        wiringpi.pwmSetRange(1024)

        #wiringpi.pinMode(Constantes.SERVO2PIN,2)
        #wiringpi.pwmSetMode(0)
        #wiringpi.pwmSetClock(400)
        #wiringpi.pwmSetRange(1024)
        #wiringpi.softPwmCreate(Constantes.SERVO2PIN, 0, 1024)

        try:
            wiringpi.pwmWrite(Constantes.SERVO1PIN, 77)
            #wiringpi.softPwmWrite(Constantes.SERVO2PIN, 42)
        except Exception as e:
            print str(e)

        self.servo1 = Servo()
        self.servo2 = Servo()
        wiringpi.pwmWrite(Constantes.SERVO1PIN, self.servo1.dt)

    def turnCam(self):
        try:
            if self.servo1.direction == Constantes.CAMLEFT:
                print "CAM LEFT"
                dtemp = self.servo1.dt + 10
                if dtemp > self.servo1.dtMax:
                    self.servo1.dt = self.servo1.dtMax
                else:
                    self.servo1.dt = dtemp
                wiringpi.pwmWrite(Constantes.SERVO1PIN, self.servo1.dt)
                print "DT = "+str(self.servo1.dt)

            elif self.servo1.direction == Constantes.CAMRIGHT:
                print "CAM RIGHT"
                dtemp = self.servo1.dt - 10
                if dtemp < self.servo1.dtMin:
                    self.servo1.dt = self.servo1.dtMin
                else:
                    self.servo1.dt = dtemp
                wiringpi.pwmWrite(Constantes.SERVO1PIN, self.servo1.dt)
                print "DT = "+str(self.servo1.dt)

            time.sleep(0.2)
        except Exception as e:
            # clean up
            wiringpi.pwmWrite(Constantes.SERVO1PIN, 0)
            print("exiting.")
            print(str(e))

    def upDownCam(self):
        try:
            if self.servo2.direction == Constantes.CAMUP:
                print "CAM UP"
                dtemp = self.servo2.dt + 10
                if dtemp > self.servo2.dtMax:
                    self.servo2.dt = self.servo2.dtMax
                else:
                    self.servo2.dt = dtemp
                wiringpi.softPwmWrite(Constantes.SERVO2PIN, self.servo2.dt)
                print "DT = "+str(self.servo2.dt)

            elif self.servo2.direction == Constantes.CAMDOWN:
                print "CAM DOWN"
                dtemp = self.servo2.dt - 10
                if dtemp < self.servo2.dtMin:
                    self.servo2.dt = self.servo2.dtMin
                else:
                    self.servo2.dt = dtemp
                wiringpi.softPwmWrite(Constantes.SERVO2PIN, self.servo2.dt)
                print "DT = "+str(self.servo2.dt)

            time.sleep(0.2)
        except Exception as e:
            # clean up
            wiringpi.softPwmWrite(Constantes.SERVO2PIN, 0)
            print("exiting.")
            print(str(e))

    def getServo1(self):
        return self.servo1

    def getServo2(self):
        return self.servo2
