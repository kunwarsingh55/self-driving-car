import lane
import motor
import camera
import cv2
import utlis

initialTrackbarVals = [31, 135, 0, 240]
utlis.initializeTrackbars(initialTrackbarVals)

while True:
    img = camera.getIMG()
    #cv2.imshow("Android_cam", img)
    cv2.imshow('Vid', img)
    cv2.waitKey(1)
    print(lane.getLaneCurve(img))
    
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
