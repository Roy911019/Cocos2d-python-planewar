# -*- coding: utf-8 -*-
# @Time    : 2021/8/28 22:01
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : loading_scene.py
# @Software: PyCharm

from pyglet import resource
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.director import director
from cocos.scenes.transitions import FadeTransition
from scene.home_scene import create_home_scene
import threading
import time

class Loadinglayer(Layer):
    def __init__(self):
        super().__init__()
        w, h = director.get_window_size()
        background = Sprite("menu.png")
        background.position = w // 2, h // 2
        self.add(background)

        anim_loading = resource.animation("loading.gif")
        sprite_anim_loading = Sprite(anim_loading,(w // 2, h // 2))
        self.add(sprite_anim_loading)


        #创建线程
        threading.Thread(target=self.thread_jump_home).start()

    def thread_jump_home(self):
        #切换场景
        time.sleep(1)
        director.push(FadeTransition(create_home_scene(),2.0))

def create_loading_scene():
    """创建读取界面"""
    loading_layer = Scene(Loadinglayer())
    return loading_layer