import cv2
import numpy as np

frameHeight = 480
frameWidth = 240
frameCounter = 0
cap = cv2.VideoCapture('v4.mp4')


def empty(e):
    pass


# New window for track bars (track bars are sliders to change values in real time)
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)

# Creat Track Bars
# ----------------("TB Name", , "Window", Starting val, Max Val)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

while True:
    # If it reaches to last frame -> Reset the frame to 0
    frameCounter += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 0

    success, img = cap.read()
    img = cv2.resize(img, (frameHeight, frameWidth))
    # We will work in HSV space
    # So converting image to HSV
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Getting track Bar values using getTrackBarPos function
    #                         ("TB name", "Window available in")
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    # Masking - using inRange function to filter out colors that are outside upper and lower values
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('Original', img)
    cv2.imshow('HSV color space', imgHsv)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    # If q is pressed then break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

"""-->ord('q') returns the Unicode code point of q
        -->cv2.waitkey(1) returns a 32-bit integer corresponding to the pressed key
            & 0xFF is a bit mask which sets the left 24 bits to zero, because ord() returns a value betwen 0 and 255, since your keyboard only has a limited character set
            Therefore, once the mask is applied, it is then possible to check if it is the corresponding key."""
