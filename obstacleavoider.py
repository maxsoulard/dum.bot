# -*- encoding: utf8 -*-

import threading
import time
from gpiodcmotors import Gpiodcmotors
from trinket import TrinketI2C


class Obstacleavoider(threading.Thread):
    def __init__(self, nom=''):
        threading.Thread.__init__(self)
        self.nom = nom
        self.Terminated = False
        self.trinket = TrinketI2C()
        self.gpiodcmotors = Gpiodcmotors()
        self.previousactions = []

    def run(self):
        vals = []
        self.gpiodcmotors.triggerForward()
        clear = True
        next = ''

        while not self.Terminated:
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
                            sltime = 0.2
                            if not clear:
                                sltime = 0.6
                                if self.previousactions[-1] == 'left':
                                    next = 'right'
                                elif self.previousactions[-1] == 'right':
                                    next = 'left'
                                    sltime = 1

                            clear = False
                            print "Obstacle droit devant ! "+str(av)
                            # Stop all current moves
                            self.gpiodcmotors.reset()
                            # going back for like 200 ms ish
                            self.__do('backward', sltime)

                            if next == 'left':
                                self.__do('left', 4)
                            elif next == 'right':
                                self.__do('right', 4)
                            else:
                                print "try left"
                                # let's try left
                                self.__do('left', 1)

                        elif not clear:
                            print "way seems clear"
                            # way seems clear, let's hit the road
                            clear = True
                            self.__do('forward', None)
                            # self.gpiodcmotors.triggerForward()
                            # previousactions.append('forward')

                        vals = []
            except:
                pass

    def __do(self, *args):
        print "__do args "+str(args[0])+" "+str(args[1])
        if args[0] == 'forward':
            self.gpiodcmotors.triggerForward()
            if args[1] is not None:
                time.sleep(args[1])

        elif args[0] == 'backward':
            self.gpiodcmotors.triggerBackward()
            if args[1] is not None:
                time.sleep(args[1])
                self.gpiodcmotors.triggerBackward()

        elif args[0] == 'right':
            if args[1] is not None:
                for i in range(0, int(args[1])):
                    self.gpiodcmotors.triggerRight()

        elif args[0] == 'left':
            if args[1] is not None:
                for i in range(0, int(args[1])):
                    self.gpiodcmotors.triggerLeft()

        self.previousactions.append(args[0])

    def stop(self):
        self.Terminated = True
        self.gpiodcmotors.reset()
