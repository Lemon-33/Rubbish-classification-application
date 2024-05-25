#视图
import tornado.web
import DAL
import json

import hashlib#导入密码加密模块
import datetime
import uuid
import base64
from test_sql import Database

from tornado.web import RequestHandler

#查找多线程之后加的一些东西
import tornado.gen
import time
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

#当前时间登录是否失效比对函数
async def compare_time(stamp1,stamp2):
    r_data_time = DAL.cal_time(stamp1,stamp2)
    return r_data_time

# conf={'host':'localhost','user':'root','pw':'whu2020','db':'test','port':3306}

class IndexHandler(RequestHandler):#继承 RequestHandler包含所有的请求和处理
    def get(self):
        self.write("Hello,world")

# class BaseHandler(RequestHandler):
#     def get_current_user(self):
#         user_id = int(self.get_secure_cookie('user'))
#         if not user_id:
#             return None
#         db=Database(conf)
#         information=db.select_one('user','userid='+user_id)#数据库里该用户的所有信息
#         if information==False:
#             self.write('没有此用户，请注册')
#             self.redirect('/register')
#         else:
#             return user_id
# 注册
async def registering(data1):  # user,password1,password2
    r_data = DAL.insert_register(data1)
    return r_data


class RegisterHandler(RequestHandler):

    # async def get(self):
    #     self.render('register.html')

    async def post(self):
        # 获取请求参数
        # 注册的时候由前端进行两个密码是否一致的判断
        # 一致则对密码进行加密,传输到后端,后端再进行加密,然后保存到数据库

        uname = self.get_argument('uname')
        password = self.get_argument('pwd')  # pasw #pwd1
        dic = {'uname': uname, 'password': password}
        data1 = json.dumps(dic)

        judge = await registering(data1)
        # 最终规划：
        # judge==0:插入成功 返回userid 客户端接收到userid之后可以跳转到登录页面
        # 以后可以用手机号

        # 测试阶段
        # if judge == 0:  # 插入成功 #密码加密之后长度过长judge为false 但是跳转到了login
        #     # self.write('已保存到数据库') okk
        #     self.redirect('/login')
        # else:
        #     # self.write('请保证两次密码相同') okk
        #     self.redirect('/register')  # 多线程

        self.write(judge)


#登录
async def logining(data2):#user,password1,password2
    r_data_login=DAL.select_login(data2)
    return r_data_login

class LoginHandler(RequestHandler):
    async def get(self):
        self.render('login.html')

    async def post(self):
        #获取请求参数
        #从前端得到user_id和加密过的密码,二次加密之后和数据库进行对比

        uname=self.get_argument('uname')#用户登录的时候用的是用户id
        password=self.get_argument('pwd')
        dic={'uname':uname,'password':password}
        data1=json.dumps(dic)
        judge = await logining(data1)
        self.write(judge)


#上传
async def uploading(data):
    r_data_upload = DAL.upload(data)
    return r_data_upload

class UploadfilesHandler(RequestHandler):
    #def get(self):
        #self.render('uploads.html')

    async def post(self):
        #获取请求参数
        #从前端得到user_id,表格类型,图片内容与格式
        uname=self.get_argument('uname')#用户登录的时候用的是用户id
        img_format = self.get_argument('img_format')
        files=self.request.files
        token = self.get_argument('token')
        stamp1 = float(token)
        stamp2 = datetime.datetime.now().timestamp()
        judge_time = await compare_time(stamp1,stamp2)
        if judge_time == 1:
            dic={'uname':uname,'files':files,'img_format':img_format}
            judge = await uploading(dic)
        else:
            judge = 'Logon_failure'
        # dic = {'uname': uname, 'files': files, 'img_format': img_format}
        # judge = await uploading(dic)
        self.write(judge)

#保存
async def saving(data2,userid,featureCoordinateXUp,featureCoordinateXDown,featureCoordinateY,c1,length,width,PictureID,img_format):#user,password1,password2
    jsonhelper = DAL.JsonHelper()
    r_data_login=jsonhelper.save(data2,userid,featureCoordinateXUp,featureCoordinateXDown,featureCoordinateY,c1,length,width,PictureID,img_format)#存到数据库
    return r_data_login

class SaveHandler(RequestHandler):
    async def get(self):
       self.render('json.html')

    async def post(self):
        testString = self.get_argument('json')
        jsonhelper = DAL.JsonHelper()
        redic = jsonhelper.dealWithRecievedJson(testString)
        testString = redic['json']
        userid = redic['userid']
        featureCoordinateXUp =redic['featureCoordinateXUp']
        featureCoordinateXDown =redic['featureCoordinateXDown']
        featureCoordinateY=redic['featureCoordinateY']
        c1=redic['c1']
        length=redic['length']
        width=redic['width']
        PictureID=redic['PictureID']
        img_format=redic['img_format']
        judge = await saving(testString,userid,featureCoordinateXUp,featureCoordinateXDown,featureCoordinateY,c1,length,width,PictureID,img_format)
        #if judge==0:
            #self.write(testString)
        self.write(judge)


#确认
async def finishing(data):
    r_data_upload = DAL.finish(data)
    return r_data_upload

class FinishHandler(RequestHandler):
    # async def get(self):
    #    self.render('json.html')

    async def post(self):
        uname = self.get_argument('uname')
        PictureID=self.get_argument('PictureID')
        ocr_result=self.get_argument('ocr_result')
        dic={'uname':uname,'PictureID':PictureID,'ocr_result':ocr_result}
        judge = await finishing(dic)
        self.write(judge)