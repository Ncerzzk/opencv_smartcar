import cv2
import numpy as np
import time
from opencv_hcm import *

cap = cv2.VideoCapture(2)
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    #img=get_chess(frame,True)
   # img=get_cross(frame)
    img=get_cross5(frame,True)
    img=None
    if img is None:
        cv2.imshow("capture", frame)
    else:
        cv2.imshow("capture",frame)
        cv2.imshow("cross",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(30) & 0xff == ord('s'):
        name=str(int(time.time()))+".jpg"
        print(name)
        cv2.imwrite(name,frame)

exit()
