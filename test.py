import cv2
import numpy as np

cam = cv2.VideoCapture(0)
prevframe = 0
mean = 0
result = 0
while(cam.isOpened()):
    ret, frame = cam.read()
    (B, G, R) = cv2.split(frame)
    mean = np.mean(R)
    result = (mean - prevframe)
    print(result)
    if (result > 0.3):
        print ("MOTION!!!!!")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    prevframe = mean
    cv2.imshow('frame', R)


    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
    
cam.release()

cv2.destroyAllWindows()