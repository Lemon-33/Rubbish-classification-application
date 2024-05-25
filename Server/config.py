#配置文件
import os
BASE_DIRS=os.path.dirname(__file__)#当前文件所在目录的绝对路径

#参数
options={
    "port": 7000
}

#配置
settings={
    "static_path":os.path.join(BASE_DIRS,"static"),
    "template_path":os.path.join(BASE_DIRS,"templates"),
    "upfile":os.path.join(BASE_DIRS,"upfile"),
    "debug":True,#修改代码之后，自动重启程序
    "cookie_secret":"rpdGCWa4RyeVszX5K2mJltPy4OdVBkLAnVRwlsWZCa0=",
}
