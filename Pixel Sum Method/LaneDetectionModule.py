import cv2
import numpy as np
import utlis
import time
curveList = []
avgVal = 10


# Get curve value from an image
def getLaneCurve(img):
    # STEP 1 - Thresholding
    # We do it based on color -> Creating a mask of white pixels
    # For more advanced edge detection we can use other algos too.
    imgThres = utlis.thresholding(img)
    cv2.imshow('Thresholding', imgThres)

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

    cv2.imshow('Warped Image', imgWarp)
    cv2.imshow('Warped Image Points', imgWarpPoints)
    cv2.imshow('Histogram full ', imgHist)
    return curve


frameCounter = 0
if __name__ == "__main__":
    cap = cv2.VideoCapture('v4.mp4')
    initialTrackbarVals = [31, 135, 0, 240]
    utlis.initializeTrackbars(initialTrackbarVals)
    while True:
        # Reset frames
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        success, img = cap.read()
        img = cv2.resize(img, (480, 240))
        cv2.imshow('Vid', img)
        time.sleep(0.05)
        cv2.waitKey(1)
        print(getLaneCurve(img))
