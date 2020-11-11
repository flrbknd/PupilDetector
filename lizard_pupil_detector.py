# -*- coding: utf-8 -*-
"""
This piece of code demonstrates pupil detection, using a stock video of a lizard.

@author: Flora
"""

import cv2
#import numpy as np

cap = cv2.VideoCapture("lizard_eye_compressed.mp4")
framecount = 0

while True:
    framecount += 1
    ret, frame = cap.read()
    if ret is False:
        break
    
    ROI = frame[800:1300, 1170:2170] #defining location of eyes, TO BE CHANGED IN CASE OF DIFFERENT VIDEO
    ROI = cv2.GaussianBlur(ROI, (9,9), 0)
    ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    #Get height and width of this region of interest:
    ROI_height = list(ROI.shape)[0]
    ROI_weight = list(ROI.shape)[1]
    
    rtrn, thres = cv2.threshold(ROI, 7, 255, cv2.THRESH_BINARY_INV) #locate the darkest areas
    contours, hierarchy = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    for c in contours:
        #Creating oval pupil shape
        try:
            ellipse = cv2.fitEllipse(c)
            cv2.ellipse(ROI, ellipse, (255), 5, cv2.LINE_AA)
        except:
            print(f"Pupil lost at frame {framecount}")
        #Creating crossing lines
        (x, y, w, h) = cv2.boundingRect(c) 
        cv2.line(ROI, (x + int(w/2), 0), (x + int(w/2), ROI_height), (255), 2)
        cv2.line(ROI, (0, y + int(h/2)), (ROI_weight, y + int(h/2)), (255), 2)
        break
    
    #fit everything to screen
    cv2.namedWindow("ROI", cv2.WINDOW_NORMAL);
    cv2.resizeWindow("ROI",(int(ROI_weight/2), int(ROI_height/2)));
    cv2.moveWindow("ROI", 0, 0)
    cv2.imshow("ROI", ROI)
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL);
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(5) #for slower framerate, raise number
    if key==27: #when 'escape' is pressed, the video quits
        break
cv2.destroyAllWindows()
