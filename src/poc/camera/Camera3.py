from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import numpy as np

import sys
sys.path.append('/usr/local/python/cv2/python-3.5/')

import cv2
import time
import subprocess
from PIL import Image
import pytesseract
import re

camera = PiCamera()
camera.resolution = (640, 384)
camera.framerate = 64
rawCapture = PiRGBArray(camera, size=(640, 384))
camera.shutter_speed = 10000
camera.iso = 1600

time.sleep(1)

pattern = re.compile("^(\d)$")
#dictionary of all contour
contours = {}
#array of edges of polygon
approx = []
#scale of the text
scale = 2
#camera
#cap = cv2.VideoCapture(0)
#camera = PiCamera()

#cap = cv2.VideoCapture('101.h264')
#cap.set(cv2.CAP_PROP_FPS, 40)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
#cap.set(cv2.CAP_PROP_EXPOSURE, 0.05); 


#stop programm
print("press q to exit")

#calculate angle
def angle(pt1,pt2,pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)

ret = True
counter = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Capture frame-by-frame
    image = frame.array
    if ret==True:
        #grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #Canny
        canny = cv2.Canny(image,80,240,3)

        #contours
        cv2.imshow('frame',image)
        cv2.imshow('canny',canny)
        contours, hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0,len(contours)):
#           #approximate the contour with accuracy proportional to
#            #the contour perimeter
             approx = cv2.approxPolyDP(contours[i],cv2.arcLength(contours[i],True)*0.02,True)
#
#            #Skip small or non-convex objects
             if(abs(cv2.contourArea(contours[i]))<100 or not(cv2.isContourConvex(approx))):
                 continue

            #ractangle
             if(len(approx) == 4):
                 x,y,w,h = cv2.boundingRect(contours[i])
#                #cv2.putText(frame,'RECT',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
#                 print("x:" + str(x) + " y:" + str(y) + " w:" + str(w) + " h:" + str(h))
                 
                 verhaeltnis = w / h
                 if (w >= 20 and h >= 20 and verhaeltnis > 0.7 and verhaeltnis < 1.3):
                 
                    u = (int) (h / 9)
                    r = (int) (2 * u)
                 
                    cropped = image[y + u: y + h - r, x + u: x + w - r]
                    current = str( time.time() )

                    cv2.imwrite( '../Pictures/cropped_img_' + current + '_.jpg', cropped )

                    image_string = pytesseract.image_to_string(cropped, config='--oem 0 --psm 5')
                    print(image_string)

               
                    counter += 1
#                    print(counter,"   cropped_img wrote")
                
#                 for huhu1 in range(0,3):
#                    for huhu2 in range(5,14):
#                        teststring = r'--oem '+str(huhu1)+' --psm '+str(huhu2);
#                       #if pattern.match(image_string):

        #Display the resulting frame
        #out.write(frame)
        rawCapture.truncate(0)
        if cv2.waitKey(27) & 0xFF == ord('q') :
            break

#When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
