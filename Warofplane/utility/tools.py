# -*- coding: utf-8 -*-
# @Time    : 2021/8/26 23:54
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : tools.py
# @Software: PyCharm

import configparser
import os
from collections import defaultdict
import pyglet

class DummyPlayer:
    def play(self):
        pass

    def pause(self):
        pass


class Sound:
    #添加音乐资源路径
    File_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    config = configparser.ConfigParser()
    config.read(File_Path + "/config.ini", encoding="utf-8")
    music_status = config.getint("setting", "music_status")
    effect_status = config.getint("setting", "effect_status")
    try:
        pyglet.resource.path.append("./resources/music")  # 指定资源文件导入位置
        pyglet.resource.reindex()
    except Exception:
        print("指定地址有误！")

    """播放背景音乐"""
    try:
        music_res = pyglet.resource.media("background.mp3", streaming=False)
    except Exception as e:
        player = DummyPlayer()
        print(e)
    else:
        player = pyglet.media.Player()
        player.queue(music_res)
        player.loop = True
        player.volume = 0.5


    try:
        music_res2 = pyglet.resource.media("home.mp3", streaming=False)
    except Exception as e:
        player2 = DummyPlayer()
        print(e)
    else:
        player2 = pyglet.media.Player()
        player2.queue(music_res2)
        player2.loop = True
        player2.volume = 0.1

    sounds_name = ["button", "bullet","enemy1_down","enemy2_down"]

    sounds = defaultdict(DummyPlayer)

    for sound in sounds_name:
        try:
            sounds[sound] = pyglet.resource.media(sound + ".wav", streaming=False)
        except Exception as e:
            print(e)


    @classmethod
    def play_music(cls,music_status):
        if music_status == 1:
            cls.player.play()
        else:
            pass

    @classmethod
    def play_music2(cls, music_status):
        if music_status == 1:
            cls.player2.play()
        else:
            pass

    @classmethod
    def play_effect(cls,name,effect_status):
        if effect_status == 1:
            cls.sounds[name].play()
        else:
            pass

    @classmethod
    def stop(cls, music_status):
        if music_status == 1:
            cls.player.pause()

    @classmethod
    def stop2(cls,scene_status):
        if scene_status == 1:
            cls.player2.pause()







