import cv2
import numpy as np


def thresholding(img):
    # Convert Image to HSV Space
    # HSL (for hue, saturation, lightness) and HSV are alternative representations of the RGB color mode

    """ cv2.cvtColor(src, code) src -> subject Image, code -> color space conversion code
    Return Value: It returns an image. """
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    """ After calling cv2.inRange, a binary mask is returned, where white pixels (255) represent pixels that fall into 
     the upper and lower limit range and black pixels (0) do not. """
    # HUE, SAT, VALUE
    lowerWhite = np.array([57, 0, 95])
    upperWhite = np.array([179, 255, 255])
    maskWhite = cv2.inRange(imgHsv, lowerWhite, upperWhite)
    # print(maskWhite) Eg - [255 255 255 ... 255 255 255] (Its actually a photo in form of array)
    return maskWhite


# Warping function - Get bird eye view of road
# Points1 - Original Points
# Points2 - Warped Points
# w,h - Final width and height that we need
"""In Perspective Transformation, we can change the perspective of a given image or video for getting better 
insights into the required information. In Perspective Transformation, 
we need to provide the points on the image from which want to gather information by changing the perspective. 
We also need to provide the points inside which we want to display our image. 
Then, we get the perspective transform from the two given sets of points and wrap it with the original image.
We use cv2.getPerspectiveTransform and then cv2.warpPerspective ."""


def warpImg(img, points, w, h):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    return imgWarp


# Trackbar for setting warping points

# Dummy Function
def nothing(e):
    pass


# 1 Initializing
def initializeTrackbars(initialTrackbarVals, wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    # '/' -> floating-point division. '//' -> integer division
    cv2.createTrackbar("Width Top", "Trackbars", initialTrackbarVals[0], wT // 2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", initialTrackbarVals[1], hT , nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", initialTrackbarVals[2], wT // 2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", initialTrackbarVals[3], hT, nothing)


# 2 Get trackbar values
def valTrackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT - widthTop, heightTop),
                         (widthBottom, heightBottom), (wT - widthBottom, heightBottom)])
    return points


# 3 Draw points to see in real time, where they're acting
def drawPoints(img, points):
    for x in range(4):
        #         image,           where to draw,               size  color     thickness
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0, 0, 255), cv2.FILLED)
    return img


def getHistogram(img, minPer=0.1, display=False, region=1):

    if region == 1:
        # Sum all the columns
        histValues = np.sum(img, axis=0)
    else:
        histValues = np.sum(img[img.shape[0]//region:, :], axis=0)

    # Get max value in the histogram to set as threshold for noise
    maxValue = np.max(histValues)

    # Use percent of the max val to set for threshold
    minValue = minPer*maxValue

    # Values above our threshold will be qualified for curve calculation
    # np.where returns list of qualified values
    indexArray = np.where(histValues >= minValue)

    # Taking average of all the indexes values
    # That will be out base point
    basePoint = int(np.average(indexArray))
    #print(basePoint)

    # Plot the base point
    if display:
        # Create an empty image using np.zeros - Return a new array of given shape and type, filled with zeros.
        imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

        # --------width-------
        # x -> Index (0 t0 479), intensity -> histVal[x]
        for x, intensity in enumerate(histValues):
            #print(x)
            # cv2.line(image, start_point,       end_point,                        color,      thickness)
            cv2.line(imgHist, (x, img.shape[0]), (x, int(img.shape[0]-intensity//255//region)), (255, 0, 255), 1)
            cv2.circle(imgHist, ((basePoint), img.shape[0]), 15, (0, 0, 155), cv2.FILLED)

        return basePoint, imgHist
    return basePoint



