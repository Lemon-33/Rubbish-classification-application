# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_design_keshe.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_interface(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 748)
        MainWindow.setStyleSheet("background-image: url(:/bgc/image_resource/bg_color.jpg);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pic = QtWidgets.QLabel(self.centralwidget)
        self.pic.setGeometry(QtCore.QRect(340, 500, 341, 231))
        self.pic.setText("")
        self.pic.setObjectName("pic")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(330, 30, 391, 61))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(28)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.litter = QtWidgets.QTableView(self.centralwidget)
        self.litter.setGeometry(QtCore.QRect(10, 110, 1001, 291))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.litter.setFont(font)
        self.litter.setStyleSheet("")
        self.litter.setObjectName("litter")
        self.clear_table = QtWidgets.QPushButton(self.centralwidget)
        self.clear_table.setGeometry(QtCore.QRect(550, 440, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        self.clear_table.setFont(font)
        self.clear_table.setObjectName("clear_table")
        self.resume_video = QtWidgets.QPushButton(self.centralwidget)
        self.resume_video.setGeometry(QtCore.QRect(110, 440, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        self.resume_video.setFont(font)
        self.resume_video.setObjectName("resume_video")
        self.backpage = QtWidgets.QPushButton(self.centralwidget)
        self.backpage.setGeometry(QtCore.QRect(760, 440, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        self.backpage.setFont(font)
        self.backpage.setObjectName("backpage")
        self.upload_files = QtWidgets.QPushButton(self.centralwidget)
        self.upload_files.setGeometry(QtCore.QRect(340, 440, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(16)
        self.upload_files.setFont(font)
        self.upload_files.setObjectName("upload_files")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "智能垃圾分类系统"))
        self.clear_table.setText(_translate("MainWindow", "清空记录"))
        self.resume_video.setText(_translate("MainWindow", "打开图片"))
        self.backpage.setText(_translate("MainWindow", "退出登录"))
        self.upload_files.setText(_translate("MainWindow", "上传图片"))
import image_rc