import cv2

import numpy as np


def get_img(text,width=80,height=60):
    text=text.strip()
    frame=text.split(" ")
    print(frame)
    cnt=0
    img=np.zeros((height,width),np.uint8)

    for i in frame:
        num=int(i,16)
        for j in range(0,8):
            row=int(cnt/width)
            col=cnt%width
            if (0x80>>j)&num:
                img[row][col]=0
            else:
                img[row][col]=255
            cnt+=1
    return img

def analize_img(img):
    width=img[0].size
    height=int(img.size/width)
    index1=0
    index2=0
    '''
    for j in range(0,height):
        for i in range(0,width):
            if img[j][i]==255:
                if index1==0:
                    index1=i
            if img[j][i]==0 and index1!=0:
                index2=i
                if index2-index1<20:
                    img[j][int((index1+index2)/2)]=0
                    break
        index1=0
    '''
    line=[]
    for i in range(0,width):
        for j in range(0,height):
            if img[j][i]==255:
                if index1==0:
                    index1=j
            if img[j][i] == 0 and index1 != 0:
                index2=j
                middle=int((index1+index2)/2)
                if len(line):
                    last=line[len(line)-1]
                    if abs(last[0]-i)<2 and abs(last[1]-middle)<2:

                        line.append((i,middle))
                        img[middle][i]=0
                        break
                    else:
                        pass
                else:
                    line.append((i, middle))
                    img[middle][i] = 0
        index1=0
    line1=line.copy()
    line.clear()
    index1=0
    index2=0

    for i in range(width-1,-1,-1):
        for j in range(0,height):
            if img[j][i]==255:
                if index1==0:
                    index1=j
            if img[j][i] == 0 and index1 != 0:
                index2=j
                middle=int((index1+index2)/2)
                if len(line):
                    last=line[len(line)-1]
                    if abs(last[0]-i<2) and abs(last[1]-middle)<2:
                        line.append((i,middle))
                        img[middle][i]=0

                else:
                    line.append((i, middle))
                    img[middle][i] = 0
                break
        index1=0
    line2=line.copy()
    line1last=line1.pop()
    line2last=line2.pop()
    heightsub_one=(line2last[1]-line1last[1])/(line2last[0]-line1last[0])
    for cnt,i in enumerate(range(line1last[0],line2last[0])):
        print(int(heightsub_one*cnt),i)
        img[line1last[1]+int(heightsub_one*cnt)][i]=0


    return img


with open("eagle.txt","r") as f:
    text=f.read()
    splited=text.split("FE 01 01 FE")
    for i in splited:
        if len(i)<1800:
            splited.remove(i)

    img=get_img(splited[7])
    img=analize_img(img)
    cv2.imshow("helo",img)
    cv2.waitKey()


def rad(x):
    return x * np.pi / 180


cv2.imshow("original", img)

# 扩展图像，保证内容不超出可视范围
img = cv2.copyMakeBorder(img, 200, 200, 200, 200, cv2.BORDER_CONSTANT, 0)
w, h = img.shape[0:2]

anglex = 35
angley = 33
anglez = 35
fov = 95
while 1:
    # 镜头与图像间的距离，21为半可视角，算z的距离是为了保证在此可视角度下恰好显示整幅图像
    z = np.sqrt(w ** 2 + h ** 2) / 2 / np.tan(rad(fov / 2))
    # 齐次变换矩阵
    rx = np.array([[1, 0, 0, 0],
                   [0, np.cos(rad(anglex)), -np.sin(rad(anglex)), 0],
                   [0, -np.sin(rad(anglex)), np.cos(rad(anglex)), 0, ],
                   [0, 0, 0, 1]], np.float32)

    ry = np.array([[np.cos(rad(angley)), 0, np.sin(rad(angley)), 0],
                   [0, 1, 0, 0],
                   [-np.sin(rad(angley)), 0, np.cos(rad(angley)), 0, ],
                   [0, 0, 0, 1]], np.float32)

    rz = np.array([[np.cos(rad(anglez)), np.sin(rad(anglez)), 0, 0],
                   [-np.sin(rad(anglez)), np.cos(rad(anglez)), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]], np.float32)

    r = rx.dot(ry).dot(rz)

    # 四对点的生成
    pcenter = np.array([h / 2, w / 2, 0, 0], np.float32)

    p1 = np.array([0, 0, 0, 0], np.float32) - pcenter
    p2 = np.array([w, 0, 0, 0], np.float32) - pcenter
    p3 = np.array([0, h, 0, 0], np.float32) - pcenter
    p4 = np.array([w, h, 0, 0], np.float32) - pcenter

    dst1 = r.dot(p1)
    dst2 = r.dot(p2)
    dst3 = r.dot(p3)
    dst4 = r.dot(p4)

    list_dst = [dst1, dst2, dst3, dst4]

    org = np.array([[0, 0],
                    [w, 0],
                    [0, h],
                    [w, h]], np.float32)

    dst = np.zeros((4, 2), np.float32)

    # 投影至成像平面
    for i in range(4):
        dst[i, 0] = list_dst[i][0] * z / (z - list_dst[i][2]) + pcenter[0]
        dst[i, 1] = list_dst[i][1] * z / (z - list_dst[i][2]) + pcenter[1]

    warpR = cv2.getPerspectiveTransform(org, dst)

    result = cv2.warpPerspective(img, warpR, (h, w))
    cv2.imshow("result", result)
    c = cv2.waitKey(30)

    # anglex += 3            #auto rotate
    # anglez += 1             #auto rotate
    # angley += 2            #auto rotate

    # 键盘控制
    if 27 == c:  # Esc quit
        break;
    if c == ord('w'):
        anglex += 1
    if c == ord('s'):
        anglex -= 1
    if c == ord('a'):
        angley += 1
        # dx=0
    if c == ord('d'):
        angley -= 1
    if c == ord('u'):
        anglez += 1
    if c == ord('p'):
        anglez -= 1
    if c == ord('t'):
        fov += 1
    if c == ord('r'):
        fov -= 1
    if c == ord(' '):
        anglex = angley = anglez = 0
    if c == ord('q'):
        print("======================================")
        print('旋转矩阵：\n', r)
        print("angle alpha: ", anglex, 'angle beta: ', angley, "dz: ", anglez, ": ", z)

cv2.destroyAllWindows()