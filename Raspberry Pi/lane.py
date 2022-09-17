import cv2
import numpy as np
import utlis
import camera
import motor
curveList = []
avgVal = 10

import RPi.GPIO as GPIO
import pigpio
import time
 
servo = 12
 
# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
 
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
 
pwm.set_PWM_frequency( servo, 50 )

#motor1 = motor.Motor(5,6,16,22,17,27)
# Get curve value from an image

curveMax = 1
curveMin = -1
curveValue = 0

servoMax = 2370
servoMin = 900

curveRange = (curveMax - curveMin)
servoRange = (servoMax - servoMin)

def getLaneCurve(img):
    # STEP 1 - Thresholding
    # We do it based on color -> Creating a mask of white pixels
    # For more advanced edge detection we can use other algos too.
    imgThres = utlis.thresholding(img)
    #cv2.imshow('Thresholding', imgThres)

    # STEP 2 - Warping - Getting Birds Eye View
    h, w, c = img.shape
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres, points, w, h)
    imgWarpPoints = utlis.drawPoints(img, points)

    # STEP 3 - getting histogram
    middlePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHistF = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint

    # STEP 4
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))

    #cv2.imshow('Warped Image', imgWarp)
    #cv2.imshow('Warped Image Points', imgWarpPoints)
    #cv2.imshow('Histogram full ', imgHist)
    
    
    #Normilization
    curve = curve/100
    if curve > 1:
        curve = 1
    if curve < -1:
        curve = -1
    return curve


frameCounter = 0
if __name__ == "__main__":
    cap = cv2.VideoCapture('v4.mp4')
    initialTrackbarVals = [31, 135, 0, 240]
    utlis.initializeTrackbars(initialTrackbarVals)
    while True:
        #Reset frames
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT)-40 == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        success, img = cap.read()
        ##img = camera.getIMG()
        img = cv2.resize(img, (480, 240))
        cv2.imshow('Vid', img)
        cv2.waitKey(1)
        curveVal = getLaneCurve(img)
        
        sen = 3.0
        #sen = 1.3  # SENSITIVITY
        #maxVAl= 1 # MAX SPEED
        #if curveVal>maxVAl:curveVal = maxVAl
        #if curveVal<-maxVAl: curveVal =-maxVAl
        #print(curveVal)
        #if curveVal>0:
          #  sen =1.7
          #  if curveVal<0.05: curveVal=0
        #else:
        #    if curveVal>-0.08: curveVal=0
        #print(curveVal)
        curveValue = curveVal * sen
        newValue = (((curveValue - curveMin) * servoRange) / curveRange) + servoMin
        if(newValue > 2500):
            newValue = 2500
        if(newValue < 500):
            newValue = 500
        
        pwm.set_servo_pulsewidth( servo, newValue ) ;
        print(curveVal)

        
        
        
        
        #cv2.waitKey(1)
