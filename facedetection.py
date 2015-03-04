import numpy as np
import cv2
from threading import Thread


class Facedetection(Thread):

    def run(self):
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

        print "face_cascade OK"

        #TODO
        jc = JpegStreamCamera("http://localhost:8083/?action=stream")
        img = jc.getImage()
        #resize img -50% to 320x240

        # img = cv2.imread('tmp.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
                print str(x)+" "+str(y)+" "+str(w)+" "+str(h)
