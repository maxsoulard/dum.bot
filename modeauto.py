# -*- encoding: utf8 -*-

import threading
import time
from trinket import TrinketI2C


class Autothread(threading.Thread):
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self.nom = nom
        self.Terminated = False
        self.trinket = TrinketI2C()

    def run(self):
        vals = []
        while not self.Terminated:
            # TODO à tester
            try:
                valtemp = self.trinket.readvalues()
                if valtemp is not None:
                    vals.append(valtemp)

                    if len(vals) == 5:
                        # if 10 values were read, calculate the average without too big values which are probably errors
                        # delete big values
                        for v in vals:
                            # TODO ignore lower and higher values
                            if len(str(v)) > 2:
                                vals.remove(v)
                        # average
                        av = sum(vals, 0.0) / len(vals)
                        # reads can now be interpreted
                        print "trinket distance average : "+str(av)
                        if av < 10:
                            # self.gpiodcmotors.triggerBackward()
                            time.sleep(5)
                            print "Obstacle droit devant ! "+str(av)
                            # self.gpiodcmotors.reset()
            except:
                pass

    def stop(self):
        self.Terminated = True
