import cv2
import numpy as np

# initilize video feed
cap = cv2.VideoCapture(0)

# loop and show video
while True:
    ret, frame = cap.read()

    # detect black square
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY_INV)

    # find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    

    # draw contours
    cv2.drawContours(frame, contours, -1, (10, 255, 0), 3)



    cv2.imshow('frame', thresh)
    if cv2.waitKey(1) == ord('q'):
        break
