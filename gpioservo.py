import time
import os
import wiringpi2 as wiringpi
from constantes import *


class ServoPwm():
    def __init__(self, pin):
        self.dtMin, self.dtMax, self.dtMed = 35, 120, 65
        self.dt = self.dtMed
        self.pin = pin
        self.direction = ''
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(18, 2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetClock(400)
        wiringpi.pwmSetRange(1024)
        try:
            wiringpi.pwmWrite(18, 40)
        except Exception as e:
            print str(e)

    def determineval(self, dtemp):
        if dtemp > self.dtMax:
            self.dt = self.dtMax
        elif dtemp < self.dtMin:
            self.dt = self.dtMin
        else:
            self.dt = dtemp

    def pwmwrite(self):
        wiringpi.pwmWrite(18, self.dt)
        print "PIN "+str(self.pin)+"DT = "+str(self.dt)


# class ServoSoftPwm():
#     def __init__(self, pin):
#         self.min, self.max, self.med = 1, 30, 15
#         self.val = self.med
#         self.pin = pin
#         self.direction = ''
#         os.system('sudo /home/pi/pi-blaster/pi-blaster '+str(self.pin))
#         valtemp = self.med / float(100)
#         os.system('echo "%d=%f" > /dev/pi-blaster' % (self.pin, valtemp))
#         time.sleep(0.2)
#         os.system('echo "%d=0" > /dev/pi-blaster' % (self.pin))
#
#     def determineval(self, dtemp):
#         if dtemp > self.max:
#             self.val = self.max
#         elif dtemp < self.min:
#             self.val = self.min
#         else:
#             self.val = dtemp
#
#     def pwmwrite(self):
#         valtemp = self.val / float(100)
#         os.system('echo "%d=%f" > /dev/pi-blaster' % (self.pin, valtemp))
#         time.sleep(0.2)
#         os.system('echo "%d=0" > /dev/pi-blaster' % (self.pin))
#         time.sleep(0.2)
#         print "PIN "+str(self.pin)+"valtemp = "+str(valtemp)+"val = "+str(self.val)


class Gpioservo():
    def __init__(self):
        # self.servo1 = ServoPwm(Constantes.SERVO1PIN)
        self.servo1 = ServoPwm(Constantes.SERVO1PIN)
        # self.servo2 = ServoSoftPwm(Constantes.SERVO2PIN)

    def turnCam(self):
        try:
            if self.servo1.direction == Constantes.CAMLEFT:
                print "CAM LEFT"
                valtemp = self.servo1.val + 5
                self.servo1.determineval(valtemp)
                self.servo1.pwmwrite()

            elif self.servo1.direction == Constantes.CAMRIGHT:
                print "CAM RIGHT"
                valtemp = self.servo1.val - 5
                self.servo1.determineval(valtemp)
                self.servo1.pwmwrite()

        except Exception as e:
            # clean up
            wiringpi.pwmWrite(Constantes.SERVO1PIN, 0)
            print("exiting.")
            print(str(e))

    def upDownCam(self):
        try:
            pass
            # if self.servo2.direction == Constantes.CAMUP:
            #     print "CAM UP"
            #     valtemp = self.servo2.val - 5
            #     self.servo2.determineval(valtemp)
            #     self.servo2.pwmwrite()
            #
            # elif self.servo2.direction == Constantes.CAMDOWN:
            #     print "CAM DOWN"
            #     valtemp = self.servo2.val + 5
            #     self.servo2.determineval(valtemp)
            #     self.servo2.pwmwrite()

        except Exception as e:
            # clean up
            print("exiting.")
            print(str(e))

    def centerCam(self):
        try:
            if self.servo1.direction == Constantes.CAMCENTER:
                valtemp = 65
                # valtemp2 = 20
                # self.servo1.determineval(valtemp)
                # self.servo1.pwmwrite()
                # self.servo2.determineval(valtemp2)
                # self.servo2.pwmwrite()

        except Exception as e:
            # clean up
            print("exiting.")
            print(str(e))
