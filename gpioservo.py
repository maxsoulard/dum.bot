from abc import abstractmethod
import time
import os
import wiringpi2 as wiringpi
from RPIO import PWM
from threading import Thread
from utils import *
from constantes import *


class Servo():
    def __init__(self, pin):
        self.direction = ''
        self.pin = pin

    @abstractmethod
    def determineval(self):
        pass

    @abstractmethod
    def pwmwrite(self):
        pass


class ServoPwm(Servo):
    def __init__(self):
        self.dtMin, self.dtMax, self.dtMed = 35, 120, 65
        self.dt = self.dtMed
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(Constantes.SERVO1PIN, 2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetClock(400)
        wiringpi.pwmSetRange(1024)
        try:
            wiringpi.pwmWrite(Constantes.SERVO1PIN, 77)
        except Exception as e:
            print str(e)

    def determineval(self, dtemp):
        if dtemp > self.dtMax:
            self.dt = self.dtMax
        elif dtemp < self.dtMin:
            self.dt = self.dtMin
        elif self.dtMed - 10 < dtemp < self.dtMed + 10:
            self.dt = self.dtMed
        else:
            self.dt = dtemp

    def pwmwrite(self):
        wiringpi.pwmWrite(self.pin, self.dt)
        print "DT = "+str(self.dt)


class ServoSoftPwm(Servo):
    def __init__(self):
        self.min, self.max, self.med = 1, 30, 15
        self.val = self.med
        os.system('sudo ~/pi-blaster/pi-blaster '+Constantes.SERVO2PIN)

    def determineval(self, dtemp):
        if dtemp > self.max:
            self.val = self.max
        elif dtemp < self.min:
            self.val = self.min
        else:
            self.val = dtemp

    def pwmwrite(self):
        val = self.val / float(100)
        os.system('echo "%d=%f" > /dev/pi-blaster' % (self.pin, val))

class Gpioservo():
    def __init__(self):
        self.servo1 = ServoPwm(Constantes.SERVO1PIN)
        self.servo2 = ServoSoftPwm(Constantes.SERVO2PIN)

    def turnCam(self):
        try:
            dtemp = self.servo1.dt
            if self.servo1.direction == Constantes.CAMLEFT:
                print "CAM LEFT"
                dtemp = self.servo1.dt + 10

            elif self.servo1.direction == Constantes.CAMRIGHT:
                print "CAM RIGHT"
                dtemp = self.servo1.dt - 10

            self.servo1.determineval(dtemp)
            self.servo1.pwmwrite()
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
                valtemp = self.servo2.val + 10
                self.servo2.determineval(valtemp)
                self.servo2.pwmwrite()

                print "DT = "+str(self.servo2.dt)

            elif self.servo2.direction == Constantes.CAMDOWN:
                print "CAM DOWN"
                valtemp = self.servo2.val - 10
                self.servo2.determineval(valtemp)
                self.servo2.pwmwrite()

                print "DT = "+str(self.servo2.dt)

            time.sleep(0.2)
        except Exception as e:
            # clean up
            print("exiting.")
            print(str(e))
