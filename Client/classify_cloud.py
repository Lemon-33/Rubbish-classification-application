from PIL import Image
import torch
from torchvision import transforms
import serial as ser
import sys
import cv2
import background_remove
import camera
import datetime
import numpy as np
import datetime
import requests

url = 'http://192.168.3.100:7000/'


# 摄像头拍摄一张照片并保存
def take_photo():
    camera.save_photo('sample.jpg')
    throw_trash_in = background_remove.detect_object('sample.jpg', 'module.jpg', 75)
    return throw_trash_in


# 读取照片（裁剪），然后识别垃圾种类并发送给ui界面与单片机
def transmit(model):
    imageNum = None
    imageClass = None

    file_send = open('file.jpg', 'rb')
    files = {'file_send': file_send}
    uploadfiles_r = requests.post(url + 'uploadfiles', files=files)
    uploadfiles_text = uploadfiles_r.text
    print(uploadfiles_text)

    # 7类
    # if imageNum == 3:
        # imageClass = 0
    # elif imageNum == 5 or imageNum == 6:
        # imageClass = 1
    # elif imageNum == 1 or imageNum == 4:
        # imageClass = 2
    # elif imageNum == 0 or imageNum == 2:
        # imageClass = 3

    if uploadfiles_text == '有害垃圾':
        imageClass = 0
    if uploadfiles_text == '厨余垃圾':
        imageClass = 1
    if uploadfiles_text == '其他垃圾':
        imageClass = 2
    if uploadfiles_text == '可回收垃圾':
        imageClass = 3

    # # 10类
    # if imageNum == 4 or imageNum == 5:
    #     imageClass = 0
    # elif imageNum == 7 or imageNum == 8 or imageNum == 9 or imageNum == 10 or imageNum == 11:
    #     imageClass = 1
    # elif imageNum == 1 or imageNum == 3 or imageNum == 6:
    #     imageClass = 2
    # elif imageNum == 0 or imageNum == 2:
    #     imageClass = 3

    imageclass = str(imageClass)
    se.write(imageclass.encode('utf-8'))  # 信息发送给单片机

    # print(imageClass)
    return imageClass
