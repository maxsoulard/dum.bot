#!/usr/bin/python
# -*- encoding: utf8 -*-

import smbus
import time

class TrinketI2C():

    def __init__(self):
        self.DEV_ADDR = 0x04
        self.bus = smbus.SMBus(1)
        self.reads = 0
        self.errs = 0
        self.reads += 1
        self.vals = []
        self.av = 0

    def readvalues(self):
        try:
            # read value from i2c (trinket)
            a_val = self.bus.read_word_data(self.DEV_ADDR, 0)
            self.vals.append(a_val)
            # print("Read value [%s]; no. of reads [%s]; no. of errors [%s]" % (a_val, reads, errs))
            # if 10 values were read, calculate the average without too big values which are probably errors
            if self.reads == 10:
                # delete big values
                for a in self.vals:
                    if len(str(a)) > 2:
                        self.vals.remove(a)
                # average
                self.av = sum(self.vals, 0.0) / len(self.vals)

                # reads can now be interpreted
                return True

            return False
        except Exception as ex:
            self.errs += 1
            print("Exception [%s]" % (ex))

        time.sleep(0.2)