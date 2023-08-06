#coding=utf-8
from distutils.core import setup

setup(
    name='MySupermath',      #对外我们模块的名字
    version='1.0',           #版本号
    description='这是第一个对外发布的模块，只用于进行测试',         #描述
    author='huanglianqi',    #作者
    author_email='1062260387@qq.com',
    py_modules=['MySuperMath.dome1','MySuperMath.dome2']      #要发布的模块
)