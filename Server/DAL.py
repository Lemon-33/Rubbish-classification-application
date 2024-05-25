from test_sql import Database
import json
import hashlib#导入密码加密模块
import datetime
import uuid
import base64
import time
import ast
from io import BytesIO
from PIL import Image
import pickle
# import pylab as plt
import cv2
from PIL import Image
import torch
from torchvision import transforms
import requests

conf={'host':'localhost','user':'root','pw':'711540','db':'test','port':3306}

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

#计算用户是否登录失效
#登陆失效返回0
#登录没有失效返回1
def cal_time(stamp1,stamp2):#stamp1是token stamp2是目前时间戳
    t1=time.localtime(stamp1)
    t2 = time.localtime(stamp2)
    t1=time.strftime("%Y-%m-%d %H:%M:%S",t1)
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", t2)
    time1=datetime.datetime.strptime(t1,"%Y-%m-%d %H:%M:%S")
    time2 = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
    diff_sec=(time2-time1).seconds
    if (diff_sec)<=3600:
        return 1
    else:
        return 0


#注册
def insert_register(json1):  # user,password1,password2
    db = Database(conf)
    data = json.loads(json1)
    judge = 1  # 保存到数据库变成0，没有保存到数据库保持1

    uname = data['uname']
    password = data['password']
    information = 'Not Found'
    # 看是否重名
    unameFound = '\'' + uname + '\''
    information = db.select_one('user', 'uname=' + unameFound)  # 数据库里该用户的所有信息

    if information == 'Not Found':  # 没有这个用户 没有重名 可以注册
        # 密码加密
        # 待加密信息为password1/password2 字符串形式
        # 创建md5对象
        hl = hashlib.md5()
        # 此处必须声明encode
        # # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
        hl.update(password.encode(encoding='utf-8'))
        result_pd = hl.hexdigest()  # 字符串

        timeStampNow = datetime.datetime.now().timestamp()  # 时间戳
        uname = '\'' + uname + '\''
        result_pd = '\'' + result_pd + '\''
        timeStampNow = '\'' + str(timeStampNow) + '\''
        password = '\'' + password + '\''
        # userid = '\'' + str(uuid.uuid1()) + '\''
        # judge = db.insert('user', {'uname': uname, 'password': result_pd, 'token': timeStampNow})
        judge = db.insert('user', {'uname': uname, 'password': password, 'token': timeStampNow})

        r_data = '1'
        if judge == 1:
            r_data = 'ACCOUNT_REGISTER_FAILED'
        if judge == 0:  # judge 等于0表示成功注册
            # r_data=str(uuid.uuid1())
            r_data = 'successful'

        return r_data

    else:  # 有这个名字 重名了
        r_data = 'Failed_name'
        return r_data

# 登录
def select_login(json2):  # userid,password
    db = Database(conf)
    data = json.loads(json2)
    # judge = 1  # 连接到数据库且查询成功变成0，否则保持1
    uname = data['uname']
    password = data['password']
    password = '\'' + password + '\''

    # 密码加密
    # 待加密信息为pswd
    # 创建md5对象
    hl = hashlib.md5()
    # 此处必须声明encode
    # # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(password.encode(encoding='utf-8'))
    input_pd = hl.hexdigest()  # 字符串

    # 数据库操作类
    db = Database(conf)
    uname = '\'' + uname + '\''
    information = 'Not Found'
    information = db.select_one('user', 'uname=' + uname)  # 数据库里该用户的所有信息

    if information == 'Not Found':
        r_data = 'No_user'

        # self.write('没有此用户，请注册')
        # self.redirect('/register')
    else:
        # 有此用户
        pw = information['password']  # 数据库里的密码
        pw = '\'' + pw + '\''
        print(pw)
        print(password)
        # if input_pd == pw:  # 密码正确
        if password == pw:
            timeStampNow = datetime.datetime.now().timestamp()  # 时间戳
            timeStampNow_save = '\'' + str(timeStampNow) + '\''
            judge = db.update('user', {'token': timeStampNow_save}, 'uname=' + uname)  # 需要测试
            if judge == 1:
                r_data = 'successful' + str(timeStampNow) # 最终阶段 返回token值(放在HTTP的header里面，后续的每一个操作都有token值)
                # r_data = 'successful'
            else:
                r_data = 'mysql mistake'
        else:
            r_data = 'Password mistake'
    return r_data

# 上传
def upload(dic):
    path = 'efficientnet-b7-Internet+v1.pth'
    model = torch.load(path)
    db = Database(conf)
    uname = dic['uname']
    files = dic['files']
    img_format = dic['img_format']
    img = files.get('file_send')  # 这里是上传图片的时候定义名字
    img = img[0]
    data = img.get('body')
    timestamp = datetime.datetime.now().timestamp()
    back = str(timestamp)  # 后缀
    # route = 'C:/Users/98686/Desktop/img/'  # 这里是图片在服务器上的保存路径
    route = './image/'
    img_route = route + back + img_format
    writer = open(img_route, 'wb')
    writer.write(data)
    writer.close()


    tfms = transforms.Compose([transforms.Resize(224), transforms.ToTensor(),
                               transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]), ])

    image = tfms(Image.open(img_route)).unsqueeze(0)  # image是用来识别的图片
    image = image.type(torch.cuda.FloatTensor)

    # Classify
    model.eval()
    with torch.no_grad():
        outputs = model(image)

    imageNum = None

    # Print predictions and send message
    for idx in torch.topk(outputs, k=1).indices.squeeze(0).tolist():
        prob = torch.softmax(outputs, dim=1)[0, idx].item()
        imageNum = idx

    item_list = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    imageClass = None
    item = item_list[imageNum]

    if imageNum == 24:
        imageClass = '有害垃圾'
    if 20 <= imageNum <= 23:
        imageClass = '厨余垃圾'
    if 10 <= imageNum <= 19:
        imageClass = '其他垃圾'
    if 0 <= imageNum <= 9:
        imageClass = '可回收垃圾'

    img_route = '\'' + img_route + '\''
    item = '\'' + item + '\''
    uname = '\'' + uname + '\''
    imageclass = '\'' + imageClass + '\''  # 这里全小写的变量代表添加了两边引号的字符串,传回前端的是没有添加引号的字符串
    judge = db.insert('Trash', {'uname':uname, 'imageRoute': img_route, 'imageClass': imageclass, 'item': item})
    if judge == 0:
        print('success')

    return imageClass



        

