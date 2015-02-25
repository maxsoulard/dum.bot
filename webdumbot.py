import os

import cherrypy
from utilssys import *
from cherrypy.lib.static import serve_file
from gpiodcmotors import *
from gpioservo import *
from trinket import *
from constantes import *


path = os.path.abspath(os.path.dirname(__file__))

class GpioApp(object):

    def __init__(self):
        self.gpiodcmotors = Gpiodcmotors()
        self.gpioservo = Gpioservo()
        self.trinket = Trinket()

    @cherrypy.expose
    def index(self):
        return serve_file(os.path.join(path, 'index.html'))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def goForward(self):
        print("FORWARD")
        self.gpiodcmotors.triggerForward()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def goBackward(self):
        print("BACKWARD")
        self.gpiodcmotors.triggerBackward()


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def turnLeft(self):
        print("LEFT")
        self.gpiodcmotors.triggerLeft()


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def turnRight(self):
        print("RIGHT")
        self.gpiodcmotors.triggerRight()

    # GESTION DES SERVOS DE LA CAM

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camUp(self):
        # Pour eviter d'envoye deux fois la meme commande
        if self.trinket.getDirection() != Constantes.CAMUP:
            self.trinket.sendCmd(Constantes.CAMUP)
        else:
            self.trinket.setDirection(None)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camDown(self):
        if self.trinket.getDirection() != Constantes.CAMDOWN:
            self.trinket.sendCmd(Constantes.CAMDOWN)
        else:
            self.trinket.setDirection(None)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camLeft(self):
        if self.gpioservo.getDirection() != Constantes.CAMLEFT:
            self.gpioservo.setDirection(Constantes.CAMLEFT)
            self.gpioservo.turnCam()
        else:
            self.gpioservo.setDirection(None)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camRight(self):
        if self.gpioservo.getDirection() != Constantes.CAMRIGHT:
            self.gpioservo.setDirection(Constantes.CAMRIGHT)
            self.gpioservo.turnCam()
        else:
            self.gpioservo.setDirection(None)

    def cancelCam(self):
        self.gpioservo.cancel()

    # FIN GESTION SERVOS CAM

    @cherrypy.expose
    def resetGpio(self):
        print("resetGpio")
        self.gpiodcmotors.reset()
        raise cherrypy.HTTPRedirect("/")


    @cherrypy.expose
    def stop(self):
        print("stop")
        #self.gpiodcmotors.stop()
        #self.gpioservo.cancel()
        Utilssys.killcampr()
        exit()



    index.exposed = True

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        },
        'global':{
            'server.socket_port': 8079
        }
    }
    cherrypy.quickstart(GpioApp(), '/', conf)
