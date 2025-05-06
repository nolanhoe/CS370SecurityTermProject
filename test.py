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
cooldown = 0
while(cam.isOpened()):
    ret, frame = cam.read()
    mean = np.mean(frame)
    result1 = abs(mean - t1)
    result2 = abs(mean - t2)
    if ((result1 > 1 or result2 > 1) and (cooldown >= 100)):
        print(f"Motion detected at {str(datetime.datetime.now())[:19]}")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cooldown = 0
    t2 = t1
    t1 = mean
    cv2.imshow('frame', frame)
    cooldown += 1
    
cam.release()

cv2.destroyAllWindows()