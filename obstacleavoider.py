# -*- encoding: utf8 -*-

import threading
import time
from gpiodcmotors import Gpiodcmotors
from trinket import TrinketI2C


class Obstacleavoider(threading.Thread):
    def __init__(self, nom=''):
        threading.Thread.__init__(self)
        self.nom = nom
        self.trinket = TrinketI2C()
        self.gpiodcmotors = Gpiodcmotors()
        self.previousactions = []
        self.paused = False
        self.state = threading.Condition()

    def run(self):
        vals = []
        clear = True
        next = ''
        self.tstarted = True
        self.resume()
        # actions counters
        self.left = 0
        self.right = 0

        while True:
            with self.state:
                if self.paused:
                    self.state.wait()
            try:
                valtemp = self.trinket.readvalues()
                if valtemp is not None:
                    vals.append(valtemp)

                    if len(vals) == 5:
                        # if 10 values were read, calculate the average without too big values which are probably errors
                        # delete big values
                        vals.remove(min(vals))
                        vals.remove(max(vals))
                        # average
                        av = sum(vals, 0.0) / len(vals)
                        # reads can now be interpreted
                        print "trinket distance average : "+str(av)
                        next = ''
                        if av < 10:
                            sltime = 0.2
                            # if there is still an obstacle
                            if not clear:
                                sltime = 0.6
                                # if bot already tried left, let's try right
                                if self.previousactions[-1] == 'left' and self.left > 4:
                                    next = 'right'
                                elif self.previousactions[-1] == 'right' and self.right > 4:
                                    next = 'left'
                                    sltime = 1

                            clear = False
                            print "Obstacle droit devant ! "+str(av)
                            # Stop all current moves
                            self.gpiodcmotors.reset()
                            # going back for like 200 ms ish
                            self.__do('backward', sltime)

                            if next == 'left':
                                self.__do('left', 3)
                            elif next == 'right':
                                self.__do('right', 3)
                            else:
                                if self.left < 2:
                                    print "try left"
                                    # let's try left
                                    self.__do('left', 1)
                                else:
                                    print "try right"
                                    # let's try left
                                    self.__do('right', 1)

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
                    self.right += 1
                    if self.right > 4:
                        self.left = 0

        elif args[0] == 'left':
            if args[1] is not None:
                for i in range(0, int(args[1])):
                    self.gpiodcmotors.triggerLeft()
                    self.left += 1
                    if self.left > 4:
                        self.right = 0

        self.previousactions.append(args[0])

    def pause(self):
        with self.state:
            self.gpiodcmotors.reset()
            self.paused = True

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()
            self.gpiodcmotors.triggerForward()

    def status(self):
        return self.paused