from opencv_hcm import *
import cv2
import numpy as np

'''
cap = cv2.VideoCapture(0)

while(1):
    ret,frame=cap.read()
    if ret:
        (x,y)=get_cross(frame,getImg=False)

'''

image=cv2.imread("cross.jpg")
cv2.imshow("test",get_cross(image,True))
cv2.waitKey()