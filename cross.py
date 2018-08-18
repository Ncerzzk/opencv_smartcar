from opencv_hcm import *
import cv2
import numpy as np
from m_serial import *
import time

cap = cv2.VideoCapture(0)

serial=MySerial(115200)
while(1):
    ret,frame=cap.read()
    if ret:
        (x,y,angle)=get_cross5(frame,getImg=False)
        serial.send_cross_data(x,y)
        time.sleep(0.05)
'''

img47=cv2.imread("cross47.jpg")
img55=cv2.imread("cross55.jpg")
cv2.imshow("47",get_cross2(img47,True))
cv2.imshow("55",get_cross2(img55,True))
cv2.waitKey()
def get_point(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x,y)

image=cv2.imread("153451797.jpg")
src=np.float32([[172,88],[64,331],[490,67],[921,193]])
H=get_H(src)

image=cv2.warpPerspective(image,H,(0,0))
cv2.imshow("test",image)
#
#cv2.imshow("test1",get_cross2(image,True))
#cv2.imshow("test",image)
cv2.setMouseCallback('test',get_point)
cv2.waitKey()
'''
