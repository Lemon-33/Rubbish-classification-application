import os
import fitz
import numpy as np
import pickle
import json
import time
import random
import cv2

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5 import QtMultimedia
from PIL import Image

from start import Ui_MainWindow
from register1 import Ui_register
from operation1 import Ui_medrecog
from interface_design_keshe import Ui_interface

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import requests
import tkinter
import tkinter.messagebox

# url of server
# url = 'http://172.28.134.190:7000/'   # 服务器端口地址
url = 'http://172.24.50.38:7000/'   # 服务器端口地址
uname=''
token = ''
id_img=''


class camera_Thread(QThread):   # 拍照识别垃圾种类的线程
    litter_Trigger = pyqtSignal(int)  # 垃圾信息信号

    def __init__(self):
        super(camera_Thread, self).__init__()

    def run(self):
        global uname
        global token
        global imgName


        img_format = '.jpg'
        file_send = open('trash.jpg', 'rb')
        files = {'file_send': file_send}
        file_info = {'uname': uname, 'img_format': img_format, 'token':token}
        uploadfiles_r = requests.post(url + 'uploadfiles', data=file_info, files=files)
        uploadfiles_text = uploadfiles_r.text
        # print(uploadfiles_text)

        if uploadfiles_text == '有害垃圾':
            imageClass = 0
        if uploadfiles_text == '厨余垃圾':
            imageClass = 1
        if uploadfiles_text == '其他垃圾':
            imageClass = 2
        if uploadfiles_text == '可回收垃圾':
            imageClass = 3

        self.litter_Trigger.emit(imageClass)

    def kill_thread(self):
        self.terminate()


class MyStandardItemModel(QStandardItemModel):     # 重载QStandardItemModel,让表格中的元素全部居中
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return QStandardItemModel.data(self, index, role)

# 登录界面
class uistart(QMainWindow, Ui_MainWindow):
  def __init__(self):
    super(uistart,self).__init__()
    self.setupUi(self)
    self.pushButton.clicked.connect(self.choose_clicked)
    self.pushButton_2.clicked.connect(self.register_clicked)

  # 登录按钮
  def choose_clicked(self):
    global uname
    global token

    # 获取用户名、密码
    uname=self.lineEdit.text()
    pwd=self.lineEdit_2.text()
    # 将用户名密码传送给后端
    data1={'uname':uname,'pwd':pwd}
    login_r = requests.post(url + 'login', data=data1)
    login_text=login_r.text
    r_cut=''
    token=''

    if (len(login_text)>10):
        # 获取前面的几个字符串
        for index1 in range(0, 10):
            r_cut = r_cut + login_text[index1]
        # print(r_cut)

        # 获取token
        for index2 in range(10, len(login_text)):
            token = token + login_text[index2]
        # print(token)
    # 根据后端的返回值做出不同的操作
    # 成功
    if(r_cut=='successful'):
      self.lineEdit.setText('')
      self.lineEdit_2.setText('')
      self.label_3.setText('')
      MyWindow.show()
      # uirecog.show()
      self.close()
    # 密码错误
    elif (login_r.text == 'Password mistake'):
      self.lineEdit_2.setText('')
      self.label_3.setText('密码错误')
    # 数据库错误
    elif(login_r.text=='mysql mistake'):
      self.label_3.setText('数据库错误')
    elif(login_r.text=='No_user'):
      self.label_3.setText('没有该用户')
      self.lineEdit.setText('')
      self.lineEdit_2.setText('')
      
  # 注册按钮
  def register_clicked(self):
    uiregister.show()
    self.close()

# 注册界面
class uiregister(QDialog,Ui_register):
  def __init__(self):
    super(uiregister,self).__init__()
    self.setupUi(self)     
    self.setWindowTitle('register window')
    self.pushButton.clicked.connect(self.regclicked)

  def regclicked(self):
    # 获取用户名、密码
    uname=self.lineEdit.text()
    pasw1=self.lineEdit_2.text()
    pasw2=self.lineEdit_3.text()
    # print('0')

    if(pasw1==pasw2):
      pwd=pasw1
      data2={'uname':uname,'pwd':pwd}
      register_r=requests.post(url + 'register', data=data2)
      # 根据后端的不同返回值有不同的操作
      # 成功
      print(register_r.text)
      if(register_r.text=='successful'):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.label_4.setText('')
        uistart.show()
        self.close()
      # 重名
      elif(register_r.text=='Failed_name'):
        self.label_4.setText('重名')
      # 注册失败
      elif(register_r.text=='ACCOUNT_REGISTER_FAILED'):
        self.label_4.setText('注册失败')
    else:
      self.label_4.setText('两次密码输入不一致')
      
#主操作界面
class MyWindow(QMainWindow, Ui_interface):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.litter_info = MyStandardItemModel()
        self.litter_info.setHorizontalHeaderLabels(['序号', '垃圾类别', '数量', '分类结果'])
        self.litter.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.litter.horizontalHeader().setStyleSheet("font:16pt '宋体';color: black;};")
        self.litter.verticalHeader().setVisible(False)  # 隐藏左侧控件自带的信号栏
        self.litter.setModel(self.litter_info)
        self.litter_num = 0  # 已经投入的垃圾的数目
        self.litter_0_num = 0  # 已经投入的有害垃圾的数目
        self.litter_1_num = 0  # 已经投入的厨余垃圾的数目
        self.litter_2_num = 0  # 已经投入的其他垃圾的数目
        self.litter_3_num = 0  # 已经投入的可回收垃圾的数目
        self.overload = [0, 0, 0, 0]  # 垃圾桶容量信息
        self.imageClass = 2  # 垃圾桶位置初始值

        # 点击按键清空表格
        self.clear_table.clicked.connect(self.clear_table_content)

        #点击按键返回登录界面
        self.backpage.clicked.connect(self.backspace)

        #点击按键上传到服务器进行识别
        self.resume_video.clicked.connect(self.getPicShow)

        # 点击按键上传图片
        self.upload_files.clicked.connect(self.upload_pic)

        self.litter_thread = camera_Thread()
        self.litter_thread.litter_Trigger.connect(self.litter_info_table_update)

    def backspace(self):
        uistart.show()
        self.close()

    def clear_table_content(self):     # 清空表格中的内容
        self.pic.setPixmap(QPixmap(""))
        self.litter_num = 0
        self.litter_0_num = 0
        self.litter_1_num = 0
        self.litter_2_num = 0
        self.litter_3_num = 0
        self.litter_info.clear()
        self.litter_info.setHorizontalHeaderLabels(['序号', '垃圾类别', '数量', '分类结果'])
        self.litter.setModel(self.litter_info)

    def getPicShow(self):
        imgType = ''
        imgName = ''
        # 获取图片
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")

        # 图片预处理
        # print(imgName)
        image = cv2.imread(str(imgName))
        cv2.imwrite('trash.jpg', image)

        pix = QPixmap('trash.jpg')
        self.pic.setPixmap(pix)
        self.pic.setScaledContents(True)

    def upload_pic(self):
        self.litter_thread.start()

# 更新垃圾信息函数
    def litter_info_table_update(self, imageClass):
        self.litter_num = self.litter_num + 1
        litter_class = ''
        self.imageClass = imageClass
        num = 0

        if self.imageClass == 0:
            litter_class = '有害垃圾'
            self.litter_0_num = self.litter_0_num + 1
            num = self.litter_0_num
        if self.imageClass == 1:
            litter_class = '厨余垃圾'
            self.litter_1_num = self.litter_1_num + 1
            num = self.litter_1_num
        if self.imageClass == 2:
            litter_class = '其他垃圾'
            self.litter_2_num = self.litter_2_num + 1
            num = self.litter_2_num
        if self.imageClass == 3:
            litter_class = '可回收垃圾'
            self.litter_3_num = self.litter_3_num + 1
            num = self.litter_3_num

        result = '识别成功'

        index = QStandardItem(str(self.litter_num))
        self.litter_info.setItem(self.litter_num - 1, 0, index)

        litter_class = QStandardItem(litter_class)
        self.litter_info.setItem(self.litter_num - 1, 1, litter_class)
        num = QStandardItem(str(num))
        self.litter_info.setItem(self.litter_num - 1, 2, num)
        result = QStandardItem(result)
        self.litter_info.setItem(self.litter_num - 1, 3, result)

        self.litter.setModel(self.litter_info)
        self.litter.scrollToBottom()           # 光标滚到表格底部
 
if __name__ == '__main__':
  QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
  app = QApplication(sys.argv)
  MyWindow = MyWindow()
  uistart=uistart()
  uiregister=uiregister()
  uistart.show()
  sys.exit(app.exec_())
