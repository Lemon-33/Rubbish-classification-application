import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
from PIL import Image
from skimage.filters import (threshold_otsu, threshold_niblack,
               threshold_sauvola)
from PIL import Image,ImageEnhance


def pixel(file_in):
    image=Image.open(file_in)
    w,h=image.size
    print('宽:'+str(w))
    print('长'+str(h))
    if (w<1800 or h<1350):
        return 0
    else:
        return 1

def brightness(img):  # 判断亮度
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 获取形状以及长宽
    img_shape = gray_img.shape
    height, width = img_shape[0], img_shape[1]
    size = gray_img.size
    # 灰度图的直方图
    hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
    # 计算灰度图像素点偏离均值(128)程序
    # a = 0
    ma = 0
    reduce_matrix = np.full((height, width), 180)
    shift_value = gray_img - reduce_matrix
    shift_sum = sum(map(sum, shift_value))
    da = shift_sum / size
    #print(da)
    # 计算偏离128的平均偏差
    for i in range(256):
        ma += (abs(i - 180 - da) * hist[i])
    m = abs(ma / size)
    #print(m)
    # 亮度系数
    k = abs(da) / m
    #print(k)
    if k[0] > 1.25:
        # 过亮
        if da > 0:
            #return -0.075*k[0]+1.075
            return da/m
        else:
            return da/m
    else:
        return 0

def bright_uniformity(file_in):  # 判断亮度均匀
    img = cv2.imread(file_in)
    unify = 1
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 获取形状以及长宽
    img_shape = gray_img.shape
    # height, width = img_shape[0], img_shape[1]
    mid = [img_shape[0] // 2, img_shape[1] // 2]
    mid1 = [img_shape[0] // 4, img_shape[1] // 4]
    mid2 = [(img_shape[0] // 4) * 3, img_shape[1] // 4]
    mid3 = [img_shape[0] // 4, (img_shape[1] // 4) * 3]
    mid4 = [(img_shape[0] // 4) * 3, (img_shape[1] // 4) * 3]
    lig = [average(gray_img, mid, 40), average(gray_img, mid1, 40), average(gray_img, mid2, 40),
           average(gray_img, mid3, 40), average(gray_img, mid4, 40)]
    k = [lig[1] / lig[0], lig[2] / lig[0], lig[3] / lig[0], lig[4] / lig[0],lig[2]/lig[1],lig[3]/lig[1],lig[4]/lig[1],lig[3]/lig[2],lig[4]/lig[2],lig[4]/lig[3]]

    for i in range(len(k)):
        if (k[i] < 0.80 or k[i]>1.25):
            unify = 0
        if k[i]>1:
            k[i]=1/k[i]
    kmin=min(k)
    return kmin, unify



def average(gray, mid, length):
    total = 0
    for i in range(mid[0] - length // 2, mid[0] + length // 2):
        for j in range(mid[1] - length // 2, mid[1] + length // 2):
            total += gray[i][j]
    lig = total / (length * length)
    return lig 

def sharp(img):
    frame =img

    resImg = cv2.resize(frame, (800, 900),interpolation=cv2.INTER_CUBIC)
    img2gray = cv2.cvtColor(resImg, cv2.COLOR_BGR2GRAY)  # 将图片压缩为单通道的灰度图

    
    res = cv2.Laplacian(img2gray, cv2.CV_64F)
    
    scoree = res.var()

    return scoree

def bization(image):
    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh_sauvola = threshold_sauvola(image)
    binary_sauvola = image > thresh_sauvola
    plt.imshow(binary_sauvola, cmap=plt.cm.gray)
    img = 255 * np.array(binary_sauvola).astype('uint8')
    #cv2.imwrite('sauvola3.jpg', img)
    #plt.title('Sauvola Threshold')
    #plt.axis('off')
    #plt.show()
    return img

def slope_point(gray_img):
    binary = gray_img
    [h, w] = binary.shape[:2]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 2))
    # 腐蚀加重表格线
    binary = cv2.erode(binary, kernel2)
    # cv2.imshow('points', binary)
    # cv2.waitKey(0)
    # 填充
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(binary, mask, (100, 100), (0, 0, 0))

    #cv2.imshow('points', binary)
    #cv2.waitKey(0)
    # 腐蚀
    erosion = cv2.erode(binary, kernel)
    # 膨胀
    dil = cv2.dilate(erosion, kernel1)
    dil = cv2.dilate(dil, kernel1)
    dil = cv2.dilate(dil, kernel1)
    # 滤波
    guassian = cv2.GaussianBlur(dil, (3, 3), 1.8)
    # cv2.imshow('points', guassian)
    # cv2.waitKey(0)

    # cv2.imshow('points', guassian)
    # cv2.waitKey(0)


    # 寻找边界
    contours, hierarchy = cv2.findContours(guassian, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    max_area = cv2.contourArea(cnt)
    for cont in contours:
        if cv2.contourArea(cont) > max_area:
            cnt = cont
            max_area = cv2.contourArea(cont)

    # define main island contour approx. and hull
    perimeter = cv2.arcLength(cnt, True)
    epsilon = 0.01 * cv2.arcLength(cnt, True)

    # 寻找角点
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    # 参考博客https: // www.it1352.com / 1701698.html

    # #创建一个全黑三通道图
    black = np.ones((h, w, 3), dtype=np.uint8)
    cv2.drawContours(black, contours, -1, (255, 255, 255), 5)
    points = cv2.drawContours(black, approx, -1, (0, 0, 255), 20)
    # 调整四个角点的坐标格式
    # 顺序左上 右上 左下 右下

    # four_points = np.vstack((approx[0][0], approx[1][0], approx[2][0], approx[3][0]))
    upleft = approx[0][0]
    upright = approx[0][0]
    downleft = approx[0][0]
    downright = approx[0][0]
    # print(approx[7][0][1])

    for i in range(0, len(approx)):
        if approx[i][0][0]+approx[i][0][1] < upleft[0]+upleft[1]:
            upleft = approx[i][0]
        if approx[i][0][0] - approx[i][0][1] > upright[0] - upright[1]:
            upright = approx[i][0]
        if approx[i][0][1] - approx[i][0][0] > downleft[1] - downleft[0]:
            downleft = approx[i][0]
        if approx[i][0][0] + approx[i][0][1] > downright[0] + downright[1]:
            downright = approx[i][0]

    four_points = np.vstack((upleft, upright, downleft, downright))



    return four_points

def slope(epoint):
    x1=epoint[0][0]
    y1=epoint[0][1]
    x2=epoint[1][0]
    y2=epoint[1][1]
    x3=epoint[2][0]
    y3=epoint[2][1]
    x4=epoint[3][0]
    y4=epoint[3][1]
    #print(epoint)
    theta1=math.atan(abs((x1-x3)/(y3-y1)))
    theta2=math.atan(abs((y2-y1)/(x2-x1)))
    theta3=math.atan(abs((x4-x2)/(y4-y2)))
    theta4=math.atan(abs((y3-y4)/(x3-x4)))
    theta_max=max(theta1,theta2,theta3,theta4)
    #print(theta1,theta2,theta3,theta4)
    theta_angle=180*theta_max/math.pi
    return theta_angle

def pcess_bright_uniformity(img):
    r = ssr(img, 100)
    r2 = mapping(r)
    r3 = r2.astype(np.uint8)
    return r3

def ssr(img, sigma):
    r = np.log(img) - np.log(cv2.GaussianBlur(img, (0,0), sigma))
    R = np.exp(r)
    return R

def mapping(r):
    max = np.max(r)
    min = np.min(r)
    result = 255*(r-min)/(max-min)
    return result

def my_perspective(src_img, points, dest_sizes):
    dst = np.float32(np.vstack(([0+50, 300], [dest_sizes[0]+50, 300], [0+50, dest_sizes[1]+300], [dest_sizes[0]+50, dest_sizes[1]+300])))
    points = np.float32(points)
    #print(dst)
    #print(points)
    m = cv2.getPerspectiveTransform(points, dst)
    return m

def guiyi(img,width,height):
    image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    #resized_image.save('guiyi.jpg')
    resized_img=cv2.cvtColor(np.array(resized_image),cv2.COLOR_RGB2BGR)
    return resized_img

def main(file_in):
    
    
    #像素点大小判断
    pixel_score=pixel(file_in)
    score1=pixel_score
    print('像素score:'+str(pixel_score))
    if (score1==1):
        print('像素大小合格'+'\n')
        #照度均匀判断
        unity_score,score3=bright_uniformity(file_in)
        print('照度均匀score:'+str(unity_score))
        if score3==1:            
            print('照度均匀合格'+'\n')
            image_zhao=cv2.imread(file_in)
            #cv2.imshow('1',image)
        elif(score3==0):
            print('照度不均匀'+'\n')
            image=cv2.imread(file_in)
            #照度均匀处理
            image_zhao=pcess_bright_uniformity(image)
            cv2.imwrite('zhao.jpg',image_zhao)
            #cv2.imshow('2',image)
        #亮度判断
        brightness_score=brightness(image_zhao)
        print('亮度score:'+str(brightness_score))
        if brightness_score==0:
            print('亮度合格'+'\n')
            image_bright=image_zhao
        else:
            #亮度处理
            if brightness_score>0:                    
                print('亮度不合格:过亮'+'\n')
                k=abs(brightness_score)
                kk=-0.079*k[0]+1.0773
            elif brightness_score<0:
                print('亮度不合格:过暗'+'\n')
                k=abs(brightness_score)
                kk=k[0]
            img1=Image.fromarray(cv2.cvtColor(image_zhao,cv2.COLOR_BGR2RGB))
            enh_bri = ImageEnhance.Brightness(img1)
            image_brightened = enh_bri.enhance(5)
            image_bright = cv2.cvtColor(np.asarray(image_brightened), cv2.COLOR_RGB2BGR)
        #cv2.imwrite('bri.jpg',image_bright)
        #锐度判断
        sharp_score=sharp(image_bright)       
        print('锐度score:'+str(sharp_score))
        if sharp_score>1000:            
            print('锐度合格'+'\n')
            image_bin=bization(image_bright)
            #cv2.imwrite('666.jpg',image_bin)
            #倾斜度判断
            epoint=slope_point(image_bin)
            #print(epoint[0][1],epoint[0])
            #返回的是倾斜的角度
            slope_score=slope(epoint)
            #print(theta)
            print('倾斜度score:'+str(slope_score))
            if slope_score<5:                
                print('倾斜度合格'+'\n')
                m = my_perspective(image_bin,epoint, (2200, 900))
                result = cv2.warpPerspective(image_bin, m, (2200+100, 900+500))
                #cv2.imwrite('result1.jpg', result)
                #像素点处理
                width=1800
                height=1350
                image_size=guiyi(result,width,height)
                #cv2.imwrite('gui22.jpg',image_size)
                return image_size
                
            else:
                print('倾斜度不合格'+'\n')
                print('重拍')
                return 1
            
        else:
            print('锐度不合格'+'\n')
            print('重拍')
            return 1
        
    elif score1==0:
        print('像素大小不合格')
        print('重拍')
        return 1
    


'''
if __name__ == '__main__':
    file_in='1.jpg'
    k=main(file_in)
    print(k)
'''
