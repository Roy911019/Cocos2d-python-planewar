# -*- coding: utf-8 -*-
# @Time    : 2021/8/28 23:12
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : home_scene.py
# @Software: PyCharm


from cocos.layer import *
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.director import director
from cocos.menu import Menu,MenuItem,verticalMenuLayout,shake,shake_back  #fixedPositionMenuLayout不指定导入可能会产生问题
from pyglet.app import exit
from scene.background_scene import create_background_scene
from scene.option_scene import create_option_scene
from cocos.scenes.transitions import FadeTRTransition,FlipAngular3DTransition
from utility.tools import Sound



class Homelayer(Layer):
    def __init__(self):
        super(Homelayer,self).__init__()


    def on_enter(self):
        """更新场景不能在子线程更新"""
        super(Homelayer,self).on_enter()
        """判断其它层是否加载完毕"""
        if len(self.get_children()) != 0 :
            return
        w, h = director.get_window_size()
        menuimg = Sprite("menu.png")
        menuimg.position = w // 2, h // 2
        self.add(menuimg,0)
        Sound.play_music2(Sound.music_status)


class MainMenu(Menu):           #菜单类自动包含了Event Handler
    def __init__(self):
        super(MainMenu,self).__init__("War of plane V2")     #SCORE在此处为title，默认为没有菜单title
        self.font_title["font_name"] = "DJB Letter Game Tiles"
        self.font_title["font_size"] = 25
        self.font_title["color"] =[176,48,96,255]
        self.font_title["bold"] = True

        self.font_item["font_name"] = "Kristen ITC"
        self.font_item["font_size"] = 38
        self.font_item["color"] = (255,255,255,255)

        self.font_item_selected["font_name"] = "Kristen ITC"
        self.font_item_selected["font_size"] = 46
        self.font_item_selected["color"] = (128, 128, 128, 255)


        self.menu_valign = "top"

        self.menu_vmargin = 50  # Variable margins for top and bottom alignment

    def on_enter(self):
        super(MainMenu,self).on_enter()
        if len(self.get_children()) != 0:
            return
        items = []
        items.append(MenuItem("Play", self.on_play_item_callback))  # 创建菜单，参数分别为菜单名和响应函数
        items.append(MenuItem("Option", self.on_option_item_callback))
        items.append(MenuItem("Quit", self.on_quit_item_callback))

        self.create_menu(items,shake(),shake_back(),
                         layout_strategy=verticalMenuLayout)

    def on_play_item_callback(self):
        Sound.play_effect("button",Sound.effect_status)
        director.push(FadeTRTransition(create_background_scene(),1.0))

    def on_option_item_callback(self):
        Sound.play_effect("button",Sound.effect_status)
        director.push(FlipAngular3DTransition(create_option_scene(),1.0))


    def on_quit_item_callback(self):
        Sound.play_effect("button",Sound.effect_status)
        exit()




def create_home_scene():
    """创建读取界面"""
    home_layer = Scene(Homelayer())
    home_layer.add(MainMenu())
    return  home_layer

