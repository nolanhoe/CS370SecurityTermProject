import cv2
import numpy as np
import datetime
from playsound3 import playsound
def record():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FPS, 30.0)

    t1 = 0
    result1 = 0
    result2 = 0
    i = 0
    cooldown = 0
    while(cam.isOpened()):
        ret, frame = cam.read()
        mean = np.mean(frame)
        result1 = abs(mean - t1)
        if (cooldown >= 75):
            if ((result1 > 0.75 or result2 > 0.75) and (cooldown >= 100)):
                print(f"Motion detected at {str(datetime.datetime.now())[:19]}")
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                cooldown = 0
                playsound("strider.mp3", block=False)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        result2 = result1
        t1 = mean
        cooldown += 1
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    record()