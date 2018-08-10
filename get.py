import cv2
import numpy as np
import time
from test import *

cap = cv2.VideoCapture(2)
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    img=get_chess(frame)
    if img is None:
        cv2.imshow("capture", frame)
    else:
        cv2.imshow("capture",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(30) & 0xff == ord('s'):
        name=str(int(time.time()))+".jpg"
        print(name)
        cv2.imwrite(name,frame)

exit()