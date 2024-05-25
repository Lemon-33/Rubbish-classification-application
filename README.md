## 智能垃圾识别系统

1.所需配置：

```
python >= 3.7
客户端必要库：pyqt5,opencv,tkinter,requests
服务器端必要库：tornado,pymysql,opencv,pytorch, requests 等等
```

代码部分由客户端和服务器端两部分组成，分别存储在Client文件夹和Server文件夹下

2.服务器端运行方法：命令行中打开Server文件夹，运行如下指令：

```
python server.py
```

为了实现上传数据库的功能，需要安装数据库mysql，然后根据所使用的数据库修改DAL.py文件中第19行中字典”conf“的内容，默认使用的是localhost下的root用户，密码为711540，使用的数据库名为“test”，之后在该数据库下执行以下两个建表语句，新版本SQL语句需要在数字上套括号：

```SQL
CREATE TABLE user(
uname VARCHAR 20,
password VARCHAR 20,
token VARCHAR 50
);

CREATE TABLE Trash(
uname VARCHAR 20,
imageRoute VARCHAR 50,
imageClass VARCHAR 10,
item VARCHAR 20
);

CREATE TABLE user(
uname VARCHAR(20),
password VARCHAR(20),
token VARCHAR(50)
);

CREATE TABLE Trash (
    uname VARCHAR(20),
    imageRoute VARCHAR(50),
    imageClass VARCHAR(10),
    item VARCHAR(20)
);
```

3.客户端运行方法：查询服务器的ip地址和在Server文件夹的config.py文件中字典“options”中的端口号，并根据这两个信息修改Client文件夹中mainw.py文件中第34行字符串变量url的值（很重要，因为服务器端运行在哪个ip地址暂时是不确定的，目前当且仅当服务器端挂在电子楼的校园网下运行时可以直接从dist文件夹中的mainw.exe文件直接启动）。之后在命令行中打开Client文件夹，运行如下指令：

```
python mainw.py
```

4.运行以上两个python文件时若报错缺少任何组件，则使用conda或者pip安装相应的库即可，改进方向：将Client文件打包成exe文件，这样就拥有运行客户端所需的环境，然后服务器端的程序只需要长时间挂在一个确定的ip地址的服务器上，则不需要进行环境配置也能运行客户端程序