# -*- encoding: utf8 -*-

import os

import cherrypy
from utilssys import *
from cherrypy.lib.static import serve_file
from gpiodcmotors import *
from gpioservo import *
from constantes import *
from obstacleavoider import Obstacleavoider


path = os.path.abspath(os.path.dirname(__file__))


class Webdumbot(object):
    def __init__(self):
        self.gpiodcmotors = Gpiodcmotors()
        self.gpioservo = Gpioservo()
        self.obstaclethread = Obstacleavoider('Auto thread')

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

    # GESTION DES SERVOS CAM

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camUp(self):
        # TODO cam up and down
        # if self.gpioservo.servo2.direction != Constantes.CAMUP:
        #     self.gpioservo.servo2.direction = Constantes.CAMUP
        #     self.gpioservo.upDownCam()
        # else:
        #     self.gpioservo.servo2.direction = None
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camDown(self):
        # TODO cam up and down
        # if self.gpioservo.servo2.direction != Constantes.CAMDOWN:
        #     self.gpioservo.servo2.direction = Constantes.CAMDOWN
        #     self.gpioservo.upDownCam()
        # else:
        #     self.gpioservo.servo2.direction = None
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camLeft(self):
        if self.gpioservo.servo1.direction != Constantes.CAMLEFT:
            self.gpioservo.servo1.direction = Constantes.CAMLEFT
            self.gpioservo.turnCam()
        else:
            self.gpioservo.servo1.direction = None

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camRight(self):
        if self.gpioservo.servo1.direction != Constantes.CAMRIGHT:
            self.gpioservo.servo1.direction = Constantes.CAMRIGHT
            self.gpioservo.turnCam()
        else:
            self.gpioservo.servo1.direction = None

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def camCenter(self):
        if self.gpioservo.servo1.direction != Constantes.CAMCENTER:
            self.gpioservo.servo1.direction = Constantes.CAMCENTER
            self.gpioservo.centerCam()
        else:
            self.gpioservo.servo1.direction = None

    def cancelCam(self):
        self.gpioservo.cancel()

    # FIN GESTION SERVOS CAM

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def resetGpio(self):
        print("resetGpio")
        self.gpiodcmotors.reset()
        raise cherrypy.HTTPRedirect("/")


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stop(self):
        print("stop")
        self.gpiodcmotors.stop()
        Utilssys.killcampr()
        exit()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def modeAuto(self):
        print("mode auto")
        # self.gpiodcmotors.triggerForward()
        # self.autothread = threading.Thread(target=self.launchautothread)
        if not self.obstaclethread.paused:
            self.obstaclethread.start()
        else:
            self.obstaclethread.resume()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def modeManuel(self):
        print("mode manuel")
        self.obstaclethread.pause()

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
    cherrypy.quickstart(Webdumbot(), '/', conf)
