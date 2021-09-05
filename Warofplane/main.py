# -*- coding: utf-8 -*-
# @Time    : 2021/8/27 22:31
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : main.py
# @Software: PyCharm


import cocos


from scene.loading_scene import create_loading_scene

if __name__ == '__main__':
    cocos.director.director.init(width=480,height=640,caption="飞机大战")
    main_scene = cocos.scene.Scene(create_loading_scene())
    cocos.director.director.run(main_scene)