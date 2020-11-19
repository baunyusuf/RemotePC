from mss import mss
import numpy as np
import cv2
import imutils

monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}


with mss() as sct:
    while "Screen capturing":
        img = np.array(sct.grab(monitor))

        cv2.imshow("OpenCV/Numpy", imutils.resize(img, width=1024, height=768))

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break