#coding:utf-8
import os
import tornado.ioloop       #开启循环，让服务一直等待请求的到来
import tornado.web          #web服务的基本功能
import tornado.httpserver
import tornado.options      #从命令行中读取设置
import config
from tornado.options import define
from application import Application

# windows 系统下 tornado 使用 使用 SelectorEventLoop
import platform

if platform.system() == "Windows":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# windows 系统下 tornado 使用 使用 SelectorEventLoop



#定义变量/端口号
define("port",default=7000,type=int,help="this is a port")


if __name__=='__main__':
    app=Application()#实例化，执行了类中的__init__

    #tornado.options.parse_command_line()#转换命令行参数

    httpServer=tornado.httpserver.HTTPServer(app)
    #绑定端口
    #httpServer.bind(8888)

    #使用变量的值
    httpServer.bind(config.options["port"])
    httpServer.start(1)#加多线程应该改成5

    tornado.ioloop.IOLoop.current().start()
