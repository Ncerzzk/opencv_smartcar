import cv2
import numpy as np
import time

def get_chess(image,minR=230,maxR=250,hough_pram2=15,getImg=True):
    image=cv2.GaussianBlur(image,(3,3),7)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.Laplacian(gray, cv2.CV_8U, gray, 3)

    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1) # 膨胀

    circles=cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,60,param1=800,param2=hough_pram2,minRadius=minR,maxRadius=maxR)
    if circles is None:
        return None
    circles=np.uint16(np.around(circles))

    cimg=cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)  # 转RGB

    for i in circles[0,:]:
        x=int(i[0])
        y=int(i[1])
        r=int(i[2])
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,0,255),2)
        cv2.circle(cimg, (i[0], i[1]), 2, (255,0,0), 2)
    if getImg==True:
        return cimg
    else:
        return (x,y,r)

class Line:
    def __init__(self,x1,y1,x2,y2):
        self.start=(x1,y1)
        self.end=(x2,y2)
        self.k=(y2-y1)/(x2-x1)
        if abs(self.k)<1:
            self.isrow=True
        else:
            self.isrow=False

        if self.isrow:
            self.lengh=abs(self.end[0]-self.start[0])
        else:
            self.lengh=abs(self.end[1]-self.start[1])


class Cross:
    def __init__(self):
        self.rows=[]
        self.cols=[]

    def add_line(self,line):
        if line.isrow==True:
            for i in self.rows:
                if self.is_same_line(i,line):
                    break
            else:
                self.rows.append(line)
        else:
            for i in self.cols:
                if self.is_same_line(i,line):
                    break
            else:
                self.cols.append(line)

    def get_cross_point(self):
        sumy=0
        if len(self.rows)==0 or len(self.cols)==0:
            raise Exception
        for i in self.rows:
            liney=(i.start[1]+i.end[1])/2
            sumy+=liney
        cross_y=int(sumy/len(self.rows))
        cnt=0

        sumx=0
        for i in self.cols:
            linex=(i.start[0]+i.end[0])/2
            sumx+=linex
            cnt+=1
        cross_x=int(sumx/len(self.cols))

        return (cross_x,cross_y)


    def is_same_line(self,line1,line2):
        if line1.isrow==True:
            if abs(line1.start[1]-line2.start[1])<10:
                return True
            else:
                return False
        else:
            if abs(line1.start[0]-line2.start[0])<10:
                return True
            else:
                return False


def get_cross(image,getImg=True):
    image=cv2.GaussianBlur(image,(3,3),7)
    height=int(image.shape[0])
    image=image[int(height/2):height-1,:]

    #cv2.illuminationChange(image,)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #ret,gray=cv2.threshold(gray,127,255,0)
    #t,contours,h=cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #gray = cv2.Laplacian(gray, cv2.CV_8U, gray, 1)
    gray=cv2.Canny(gray,200,200)

    cimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    lines=cv2.HoughLinesP(gray,1,np.pi/180,80,minLineLength=150,maxLineGap=400)

    if len(lines) <4:
        return (0,0)

    cross=Cross()

    for j in lines:
        i=j[0]
        x1=i[0]
        y1=i[1]
        x2=i[2]
        y2=i[3]
        temp=Line(x1,y1,x2,y2)
        cross.add_line(temp)
        cv2.line(cimg,(x1,y1),(x2,y2),(0,255,0),2)

    #cv2.drawContours(cimg, contours, -1, (0, 255, 0), 2)
    try:
        (x,y)=cross.get_cross_point()
        cv2.circle(cimg,(x,y),2,(255,255,0),2)
    except:
        return (0,0)

    if getImg==True:
        return cimg
    else:
        return (x,y)


