import subprocess
from constantes import *

class Utilssys:
    @staticmethod
    def killcampr():
        # Kill le processus de streaming du module camera
        p = subprocess.Popen("sudo fuser -k "+Constantes.PORT_CAM_PR+"/tcp", stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()