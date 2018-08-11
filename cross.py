from opencv_hcm import *
import cv2
import numpy as np
#from m_serial import *
import time

'''
cap = cv2.VideoCapture(0)

serial=MySerial(115200)
while(1):
    ret,frame=cap.read()
    if ret:
        cross=get_cross(frame,getImg=True)
    serial.send_cross_data(5,1)
    time.sleep(5)


'''

def get_point(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x,y)

image=cv2.imread("1533967630.jpg")
src=np.float32([[275,0],[316,0],[204,479],[384,479]])
dst=np.float32([[275,0],[316,0],[275,479],[316,479]])
H=cv2.getPerspectiveTransform(src,dst)
image=cv2.warpPerspective(image,H,(0,0))

image=cv2.imread("1533967822.jpg")
image=cv2.warpPerspective(image,H,(0,0))
cv2.imshow("test1",get_cross(image,True))

cv2.setMouseCallback('test',get_point)
cv2.waitKey()