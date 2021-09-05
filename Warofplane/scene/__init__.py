# -*- coding: utf-8 -*-
# @Time    : 2021/8/26 23:47
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : __init__.py.py
# @Software: PyCharm

"""
直接在在此添加各路径
"""



import pyglet

try:
    pyglet.resource.path.append("./resources/image/")     #添加文件搜索路径
    pyglet.resource.reindex()       #重新定义资源属性
except Exception as e:
    print("导入图片库文件失败")


try:
    pyglet.font.add_directory("./resources/font/")  # 添加字体路径
except Exception as e:
    print("导入字体库文件失败")