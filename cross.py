from opencv_hcm import *
import cv2
import numpy as np
#from m_serial import *
import time


cap = cv2.VideoCapture(0)
src=np.float32([[1,141],[172,385],[281,95],[611,146]])
H=get_H(src)

serial=MySerial(115200)
while(1):
    ret,frame=cap.read()
    if ret:
        frame=cv2.warpPerspective(frame,H,(0,0))
        cross=get_cross2(frame,getImg=True)
    serial.send_cross_data(5,1)
    time.sleep(0.05)



'''
def get_point(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x,y)

image=cv2.imread("1534502104.jpg")
#src=np.float32([[275,0],[316,0],[204,479],[384,479]])
#dst=np.float32([[275,0],[316,0],[275,479],[316,479]])
src=np.float32([[73,277],[348,233],[568,263],[235,477]])
dst=np.float32([[73,233],[348,233],[348,477],[77,477]])
cv2.imshow("test",image)
H=cv2.getPerspectiveTransform(src,dst)
image=cv2.warpPerspective(image,H,(0,0))
#
#cv2.imshow("test1",get_cross2(image,True))
#cv2.imshow("test",image)
cv2.setMouseCallback('test',get_point)
cv2.waitKey()
'''
