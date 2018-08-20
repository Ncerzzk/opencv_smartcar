from opencv_hcm import *
import cv2
import numpy as np
from m_serial import *
import time

cap_cross = cv2.VideoCapture(0)

cap_chess = cv2.VideoCapture(1)

serial=MySerial(115200)
while(1):
    ret,frame=cap_cross.read()
    if ret:
        cross=get_cross5(frame,getImg=False)
        if cross is not None:
            serial.send_cross_data(cross[0],cross[1],cross[2])
        else:
            serial.send_cross_data(0,0,0)
            print("no line!\r\n")
    ret_frame=cap_chess.read()
    if ret:
        chess=get_chess(frame,getImg=False)
        if chess is not None:
            serial.send_chess_data(chess[0],chess[1],chess[2])
        else:
            serial.send_chess_data(0,0,0)
            print("no chess!\r\n")


