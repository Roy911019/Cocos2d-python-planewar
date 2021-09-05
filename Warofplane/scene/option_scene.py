# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 20:50
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : option_scene.py
# @Software: PyCharm

import configparser
import os
from cocos.layer import *
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.director import director
from cocos.menu import Menu,MenuItem,EntryMenuItem,ToggleMenuItem,verticalMenuLayout,zoom_in,zoom_out  #fixedPositionMenuLayout不指定导入可能会产生问题
from utility.tools import Sound



class Homelayer(Layer):
    def __init__(self):
        super(Homelayer,self).__init__()

    def on_enter(self):
        super(Homelayer,self).on_enter()
        """更新场景不能在子线程更新"""
        if len(self.get_children()) != 0 :
            return
        w, h = director.get_window_size()
        menuimg = Sprite("menu.png")
        menuimg.position = w // 2, h // 2
        self.add(menuimg)




class OptionMenu(Menu):           #菜单类自动包含了Event Handler
    def __init__(self):
        super().__init__("Option")     #SCORE在此处为title，默认为没有菜单title
        self.font_title["font_size"] =64
        self.font_title["color"] =[176,48,96,255]
        self.font_title["bold"] = True

        self.font_item["font_size"] = 38
        self.font_item["color"] = (255,255,255,255)

        self.font_item_selected["font_size"] = 38
        self.font_item_selected["color"] = (128, 128, 128, 255)


    def on_enter(self):
        super(OptionMenu,self).on_enter()
        if len(self.get_children()) != 0:
            return
        # 设置最高分纪录
        File_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        config = configparser.ConfigParser()
        config.read(File_Path + "/config.ini", encoding="utf-8")
        best_score = config.getint("setting", "best_score")
        user_name = config.get("setting", "user_name")

        items = []
        items.append(EntryMenuItem("Name:", self.on_name, user_name))  # 创建菜单，参数分别为菜单名和响应函数
        items.append(MenuItem("Record:" + str(best_score), self.on_score))
        items.append(ToggleMenuItem("Music:", self.on_music, Sound.music_status))
        items.append(ToggleMenuItem("Effect:", self.on_effect, Sound.effect_status))
        items.append(MenuItem("Back", self.on_back))
        self.create_menu(items,zoom_in(),zoom_out(),
                         layout_strategy=verticalMenuLayout)  # 菜单内容及菜单被选中时的特效

    def on_name(self,value):
        name = value
        Sound.play_effect("button", Sound.effect_status)
        File_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        config = configparser.ConfigParser()
        config.read(File_Path + "/config.ini", encoding="utf-8")
        config.set("setting", "user_name", str(name))
        with open('config.ini', 'w+') as file:
            config.write(file)

    # def on_level(self,idx):
    #     pass
    #     print(idx)

    def on_score(self):
        pass

    def on_music(self, value):
        judge = value
        Sound.play_effect("button", Sound.effect_status)
        File_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        config = configparser.ConfigParser()
        config.read(File_Path + "/config.ini", encoding="utf-8")
        config.set("setting", "music_status", str(judge))
        with open('config.ini', 'w+') as file:
            config.write(file)
        Sound.music_status = judge

    def on_effect(self,value):
        judge = value
        Sound.play_effect("button",Sound.effect_status)
        File_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        config = configparser.ConfigParser()
        config.read(File_Path + "/config.ini", encoding="utf-8")
        config.set("setting", "effect_status",str(judge))
        with open('config.ini', 'w+') as file:
            config.write(file)
        Sound.effect_status = judge

    def on_back(self):
        Sound.play_effect("button", Sound.effect_status)
        director.pop()

def create_option_scene():
    """创建读取界面"""
    option_layer = Scene(Homelayer())
    option_layer.add(OptionMenu())
    return  option_layer
