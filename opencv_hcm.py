import cv2
import numpy as np
import time
import math

def get_H(src_list):
    left_up=src_list[0]
    left_down=src_list[1]
    right_up=src_list[2]
    right_down=src_list[3]

    dst=list()
    '''
    dst.append([left_down[0],right_up[1]])
    dst.append([left_down[0],left_down[1]])
    dst.append([right_up[0],right_up[1]])
    dst.append([right_up[0],left_down[1]])
    '''

    dst.append([left_up[0], right_up[1]])
    dst.append([left_up[0], left_down[1]])
    dst.append([right_up[0], right_up[1]])
    dst.append([right_up[0], left_down[1]])

    dst=np.array(dst)
    return cv2.getPerspectiveTransform(src_list,dst)


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
    def __init__(self,x1=0,y1=0,x2=0,y2=0,k=None,b=None):
        self.start=(x1,y1)
        self.end=(x2,y2)
        if k is None:
            self.k=(y2-y1)/(x2-x1)
        else:
            self.k=k
        if b is None:
            self.b=-self.k*x1+y1
        else:
            self.b=b
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
            if len(self.rows)>=2:
                return None
            for i in self.rows:
                if self.is_same_line(i,line):
                    break
            else:
                self.rows.append(line)
        else:
            if len(self.cols)>=2:
                return None
            for i in self.cols:
                if self.is_same_line(i,line):
                    break
            else:
                self.cols.append(line)

    def get_cross_point(self):
        if len(self.rows)+len(self.cols)==3:
            if len(self.rows)==1:
                width=abs(self.cols[0].start[0]-self.cols[1].start[0])
                width=int(width)
                new_row=Line(x1=self.rows[0].start[0],
                             y1=self.rows[0].start[1]+width,
                             x2=self.rows[0].end[0],
                             y2=self.rows[0].end[1]+width)
                self.add_line(new_row)
            else:
                width=abs(self.rows[0].start[1]-self.rows[1].start[1])
                width=int(width)
                new_col=Line(x1=self.cols[0].start[0]-width,
                             y1=self.cols[0].start[1],
                             x2=self.cols[0].end[0]-width,
                             y2=self.cols[0].end[1])
                self.add_line(new_col)
        if len(self.rows)!=2 or len(self.cols)!=2:
            raise Exception
        temp_k=(self.rows[0].k+self.rows[1].k)/2
        temp_b=(self.rows[0].b+self.rows[1].b)/2
        row_line=Line(k=temp_k,b=temp_b)

        inf=float("inf")
        if abs(self.cols[0].k)==inf or abs(self.cols[1].k)==inf: # 处理垂直的直线的情况
            x=(self.cols[0].start[0]+self.cols[1].start[0])/2
            y=row_line.k*x+row_line.b
            x=int(x)
            y=int(y)
        else:
            temp_k = (self.cols[0].k + self.cols[1].k) / 2
            temp_b = (self.cols[0].b + self.cols[1].b) / 2
            col_line = Line(k=temp_k, b=temp_b)
            x,y=self.get_2lines_cross(row_line,col_line)
        angle=math.atan(self.cols[0].k)*180/math.pi
        return (x,y,angle)




    def get_2lines_cross(self,line1,line2):
        x=(line2.b-line1.b)/(line1.k-line2.k)
        y=line1.k*x+line1.b

        x=int(x)
        y=int(y)
        return (x,y)


    def is_same_line(self,line1,line2):
        if line1.isrow==True:
            if abs(line1.b-line2.b)<10:
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
    image=image[int(height/2):height-1,:]  # 切片，不要的扔掉

    #cv2.illuminationChange(image,)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #ret,gray=cv2.threshold(gray,127,255,0)
    t,contours,h=cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # 找外轮廓
    #gray = cv2.Laplacian(gray, cv2.CV_8U, gray, 1)
    gray=cv2.Canny(gray,100,100)
    cv2.drawContours(gray,contours,-1,(0,0,0),2)  #去掉外轮廓 实际上是为了去掉透视后的黑边
    cv2.imshow("xx",gray)
    cimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)

    lines=cv2.HoughLinesP(gray,1,np.pi/180,120,minLineLength=150,maxLineGap=200)
    if lines is None:
        return None
    cross=Cross()

    for j in lines:
        i=j[0]
        x1=i[0]
        y1=i[1]
        x2=i[2]
        y2=i[3]
        temp=Line(x1,y1,x2,y2)
        cross.add_line(temp)
        cv2.line(cimg,(x1,y1),(x2,y2),(0,255,0),1)
    #cv2.drawContours(cimg, contours, -1, (0, 255, 0), 2)
    try:
        (x,y,angle)=cross.get_cross_point()  # 如果没找够4条线，这里会抛出异常
        cv2.circle(cimg,(x,y),2,(255,255,0),2)
    except:
        return None 

    if getImg==True:
        return cimg
    else:
        return (x,y)


SRC=np.float32([[107,210],[415,371],[355,187],[635,236]])
H=get_H(SRC)




def get_cross2(image,getImg=True):

    height=int(image.shape[0])
    width=int(image.shape[1])

    #image=image[0:int(height/12)*6,:]  # 切片，不要的扔掉

    #image=image[0:int(height/12)*6:,int(width/4):width]

    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    t,contours,h=cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # 找外轮廓
    #gray = cv2.Laplacian(gray, cv2.CV_8U, gray,5 )
    ret, gray = cv2.threshold(gray, 170, 255, 0)
    gray = cv2.Canny(gray, 80, 50)


    cv2.drawContours(gray,contours,-1,(0,0,0),2)  #去掉外轮廓 实际上是为了去掉透视后的黑边


    kernel = np.ones((5, 5), np.uint8)
    #gray = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)   #形态学梯度
    #gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    #gray = cv2.dilate(gray, kernel, iterations=1)

    cimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    gray = cv2.dilate(gray, kernel, iterations=1)
    cross=Cross()
    lines=cv2.HoughLinesP(gray,1,np.pi/180,100,minLineLength=100,maxLineGap=300)
    if lines is None:
        if getImg==True:
            return cimg
        else:
            return None
    for j in lines:
        i=j[0]
        x1=i[0]
        y1=i[1]
        x2=i[2]
        y2=i[3]
        temp=Line(x1,y1,x2,y2)
        cross.add_line(temp)
        cv2.line(cimg,(x1,y1),(x2,y2),(0,255,0),1)

    try:
        (x,y,angle)=cross.get_cross_point()  # 如果没找够4条线，这里会抛出异常
        cv2.circle(cimg,(x,y),2,(255,255,0),2)
    except:
        if getImg==True:
            return cimg
        else:
            return None
    if getImg==True:
        print(x,y,angle)
        return cimg
    else:
        return (x,y,angle)

def get_cross3(image, getImg=True):
    # 想通过找到逆透视的偏移，来修正地不平，废弃
    height=image.shape[0]
    width=image.shape[1]

    image=image[int(height/3):height,:]
    gray=image

    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ret, gray = cv2.threshold(gray, 130, 255, 1)
    gray = cv2.Canny(gray, 200, 100)
    cv2.imshow("ca2n",gray)
    #cv2.imshow("can",gray)
    #cv2.waitKey()
    #cimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cimg=image
    cross = Cross()
    lines = cv2.HoughLinesP(gray, 1, np.pi / 180, 100, minLineLength=300, maxLineGap=300)
    if lines is None:
        if getImg == True:
            return cimg
        else:
            return None
    my_lines = []
    for j in lines:
        i = j[0]
        x1 = i[0]
        y1 = i[1]
        x2 = i[2]
        y2 = i[3]
        temp = Line(x1, y1, x2, y2)
        my_lines.append(temp)
        cross.add_line(temp)
        cv2.line(cimg, (x1, y1), (x2, y2), (0, 255, 0), 1)
    cv2.imshow('test2', cimg)
    point = cross.get_2lines_cross(my_lines[0], my_lines[1])
    new_src = SRC + point - SRC[0]
    new_src = np.float32(new_src)
    new_H = get_H(new_src)

    gray = cv2.warpPerspective(gray, new_H, (0, 0))

    gray=gray[:,int(width/4):width]

    lines = cv2.HoughLinesP(gray, 1, np.pi / 180, 300, minLineLength=300, maxLineGap=300)
    cimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cross = Cross()
    if lines is None:
        if getImg == True:
            return cimg
        else:
            return None
    for j in lines:
        i = j[0]
        x1 = i[0]
        y1 = i[1]
        x2 = i[2]
        y2 = i[3]
        temp = Line(x1, y1, x2, y2)
        cross.add_line(temp)
        cv2.line(cimg, (x1, y1), (x2, y2), (0, 255, 0), 1)
    try:
        (x,y,angle)=cross.get_cross_point()  # 如果没找够4条线，这里会抛出异常
        cv2.circle(cimg,(x,y),2,(255,255,0),2)
    except:
        if getImg==True:
            return cimg
        else:
            return None
    if getImg==True:
        print(x,y,angle)
        return cimg
    else:
        return (x,y,angle)

def get_cross4(image,getImg=True):
    #想通过找数字的中心，来修正偏差
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #gray = cv2.Canny(gray, 200, 200)
    ret, gray = cv2.threshold(gray, 200, 255, 1)
    cv2.imshow("shold",gray)
    i,cs,h=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for c in cs:
        x,y,w,h=cv2.boundingRect(c)
        area=cv2.contourArea(c,True)
        print(area)
        if cv2.contourArea(c,True) <4000:
            continue
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        rect=cv2.minAreaRect(c)
        box=cv2.boxPoints(rect)
        box=np.int0(box)
        cv2.drawContours(image,[box],0,[0,0,255],3)

def get_cross5(image,getImg=True):
    height=int(image.shape[0])
    width=int(image.shape[1])

    #image=image[0:int(height/12)*6,:]  # 切片，不要的扔掉
    image = cv2.warpPerspective(image, H, (0, 0))
    #image=image[0:int(height/12)*6:,int(width/4):width]
    #image=image[int(height/12)*:height,:]
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    t,contours,h=cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # 找外轮廓
    #gray = cv2.Laplacian(gray, cv2.CV_8U, gray,5 )
    #ret, gray = cv2.threshold(gray, 140, 255, 0)
    gray=cv2.Canny(gray,300,200)
    cv2.drawContours(gray,contours,-1,(0,0,0),2)  #去掉外轮廓 实际上是为了去掉透视后的黑边
    kernel = np.ones((5, 5), np.uint8)
    #gray = cv2.dilate(gray, kernel, iterations=1)

    lines = cv2.HoughLinesP(gray, 1, np.pi / 180, 100, minLineLength=200, maxLineGap=300)
    cimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cross = Cross()
    if lines is None:
        if getImg == True:
            return cimg
        else:
            return None
    for j in lines:
        i = j[0]
        x1 = i[0]
        y1 = i[1]
        x2 = i[2]
        y2 = i[3]
        temp = Line(x1, y1, x2, y2)
        if abs(temp.k)<1:
            if y1>300:
                cross.add_line(temp)
        else:
            cross.add_line(temp)
        cv2.line(cimg, (x1, y1), (x2, y2), (0, 255, 0), 1)
    try:
        (x, y, angle) = cross.get_cross_point()  # 如果没找够4条线，这里会抛出异常
        cv2.circle(cimg, (x, y), 2, (255, 255, 0), 2)
        cv2.imshow('test', cimg)
    except:
        if getImg == True:
            return cimg
        else:
            return None
    if getImg == True:
        print(x, y, angle)
        return cimg
    else:
        return (x, y, angle)

'''
#src=np.float32([[116,113],[346,267],[277,84],[601,132]])
#dst=np.float32([[116,84],[116,267],[277,84],[277,267]])
#cv2.imshow("test",image)
#src=np.float32([[31,92],[27,327],[395,42],[702,96]])
#H#=get_H(src)

image=cv2.imread("1534553104.jpg")
#image=cv2.warpPerspective(image,H,(0,0))

cross=get_cross5(image,True)
if cross is not None:
    cv2.imshow("test1",cross)

#cv2.setMouseCallback('test',get_point)
cv2.waitKey()
'''
