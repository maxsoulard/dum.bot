import time
from Adafruit_I2C import Adafruit_I2C
from constantes import *

class Trinket():
    def __init__(self):
        self.i2c = Adafruit_I2C(Constantes.I2C_TRINKET1ADR)

    def __writeI2C(self):
        # Ecriture de deux bytes, le registre (ici à 0) et la valeur hexa 0x40
        self.i2c.write8(0, Constantes.I2C_INIT)

        # Donner un delais au périphérique I2C pour qu'il soit prêt a recevoir
        # une nouvelle communication... sinon on recoit l'erreur
        #   Error accessing 0x04: Check your I2C address
        time.sleep(Constantes.I2C_TIMESLEEP)

        if self.direction is not None and len(self.direction) == 1:
            self.i2c.write8(0x02, ord(str(self.direction)))
            time.sleep(Constantes.I2C_TIMESLEEP)

    def sendCmd(self, direction=None):
        self.direction = direction
        # TODO à completer
        # TODO A simplifier, en cas d'erreur I2C non dispo on réessaye
        try:
            self.__writeI2C()
        except IOError, err:
            time.sleep(Constantes.I2C_TIMESLEEP)
            try:
                self.__writeI2C()
            except IOError, err:
                print "ERROR I2C TRINKET"
