import subprocess
from constantes import *

class Utilssys:
    @staticmethod
    def killcampr():
        print "Kill du processus de streaming du module pi camera"
        p = subprocess.Popen("sudo fuser -k "+str(Constantes.PORT_CAM_PR)+"/tcp", stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
