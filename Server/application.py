# 路由
# URL
import tornado.web
import config
# import pymysql
from views import index


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', index.IndexHandler),
            # 注册
            (r'/register', index.RegisterHandler),
            # 登录
            (r'/login', index.LoginHandler),
            # 上传文件
            (r'/uploadfiles', index.UploadfilesHandler),
        ]

        # 父类的init函数，参数为handlers
        # autoreload和debug是多线程autoreload=False,debug=False
        super(Application, self).__init__(handlers, **config.settings),
        # **config.settings相当于把里面的参数提取出来了
