import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

print "face_cascade OK"

#TODO
#jc = JpegStreamCamera("http://192.168.1.15:8083/?action=stream")
#img = jc.getImage().save("tmp.jpg")

img = cv2.imread('test3.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
        print str(x)+" "+str(y)+" "+str(w)+" "+str(h)
