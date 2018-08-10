from opencv_hcm import *
import cv2
import numpy as np
from m_serail import *

cap = cv2.VideoCapture(0)

serial=MySerial(115200)

while(1):
    ret,frame=cap.read()
    if ret:
        cross=get_cross(frame,getImg=True)
        if cross is not None:
            (x,y)=cross
            serial.send_cross_data(x,y)



