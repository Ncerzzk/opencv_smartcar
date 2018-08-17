import cv2
import numpy as np
import time
from opencv_hcm import *

cap = cv2.VideoCapture(2)
src=np.float32([[1,141],[172,385],[281,95],[611,146]])
H=get_H(src)
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    #img=get_chess(frame,True)
   # img=get_cross(frame)
    frame=cv2.warpPerspective(frame,H,(0,0))
    img=get_cross2(frame,True)
    #img=frame
    img=None
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
