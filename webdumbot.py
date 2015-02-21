import os

import cherrypy
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


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camUp(self):
        print("TODO")
        # self.gpiodcmotors.triggerRight()


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camDown(self):
        print("TODO")
        # self.gpiodcmotors.triggerRight()


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camLeft(self):
        # self.gpioservo.setDirection('left')
        self.trinket.sendCmd(Constantes.CAMLEFT)
        self.gpioservo.turnCam()


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camRight(self):
        gpioservo = Gpioservo()
        if gpioservo.getDirection() == 'right':
            self.cancelCam()
        else:
            gpioservo.setDirection('right')
            gpioservo.start()

    def cancelCam(self):
        gpioservo = Gpioservo()
        gpioservo.cancel()

    @cherrypy.expose
    def resetGpio(self):
        print("resetGpio")
        self.gpiodcmotors.reset()
        raise cherrypy.HTTPRedirect("/")



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
