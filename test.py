import cv2
import numpy as np
import datetime

cam = cv2.VideoCapture(0)
t1 = 0
t2 = 0
mean = 0
result1 = 0
result2 = 0
i = 0
while (i < 100):
    ret, frame = cam.read()
    cv2.imshow('frame', frame)
    i += 1
while(cam.isOpened()):
    ret, frame = cam.read()
    mean = np.mean(frame)
    result1 = abs(mean - t1)
    result2 = abs(mean - t2)
    if (result1 > 1 or result2 > 1):
        print(f"Motion detected at {datetime.datetime.now()}")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    t2 = t1
    t1 = mean
    cv2.imshow('frame', frame)
    
cam.release()

cv2.destroyAllWindows()