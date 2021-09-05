# -*- coding: utf-8 -*-
# @Time    : 2021/8/27 22:37
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : background.py
# @Software: PyCharm


from collections import defaultdict
import configparser
import os
from pyglet.window import key
import pyglet
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.director import director


from utility.tools import Sound
from sprite.game_sprite import Fight,Bullet
from sprite.enemy_sprite import Enemy,Enemy_die,Supply
from cocos.text import Label


class Background(Layer):
    is_event_handler = True
    scene_status = True
    def __init__(self):
        super(Background, self).__init__()

        self.width,self.height = director.get_window_size()
        self.init_background()
        self.bullet_dt = 0    #子弹间隔
        self.enemy_dt = 0
        self.score =  0

        self.supply_score = 0
        self.add_supply = 1
        self.supply_dt = 0
        self.bullet_type = 1

        self.pressed = defaultdict(int)  # 获得按键字典
        self.schedule(self.update)  # 任务调度
        #
        # self.cm = CollisionManagerGrid(0, 480, 0, 640, 32 * 1.25,
        #                                32 * 1.25)  # 参数为待检测区域xmin,xmax,ymin,ymax,cell宽和cell高，待检测cell一般设为cell的1.25倍
        self.init_sprite_flight()
        self.init_statusbar()
        self.init_scorehub()
        self.init_lifehub()


        self.BG_music()
        self.pause_status = 0 #1暂停，0继续

    #得到键盘的输入
    def on_key_press(self, k, _):   #判断是否按了相应的键
        self.pressed[k] = 1


    def on_key_release(self, k, _):
        self.pressed[k] = 0

    def update(self, dt):
        """游戏调度"""
        if self.pause_status == 0:  # 暂停时自己不动
            self.flight.move(self.pressed)     #随时间更新飞机的运动
        self.bullet_dt += dt                     #获取两个子弹的间隔满足时间
        self.enemy_dt += dt
        if self.bullet_type == 2:
            self.supply_dt += dt
        if self.supply_dt >= 10:
            self.bullet_type = 1
            self.supply_dt = 0
        if self.pressed[key.A] and self.bullet_dt > 0.3 and self.pause_status == 0:      #暂停时不出现子弹:
            if self.bullet_type == 1:
                self.init_sprite_bullet()
                self.bullet.shoot_bullet(self.flight)
                self.bullet_dt = 0
            else:
                self.init_sprite_bullet()
                self.bullet1.shoot_bullet2(self.flight)
                self.bullet2.shoot_bullet3(self.flight)
                self.bullet_dt = 0
        if self.enemy_dt> 3:
            if self.pause_status == 0:          #暂停时不出现敌人
                self.init_sprite_enemy()
            self.enemy_dt = 0

        if self.supply_score >= 10:
            self.init_sprite_supply()
            self.supply_score = 0

        for node in self.get_children():       #寻找子节点并加入到待测区域中
            if isinstance(node,Bullet) and not node.visible or isinstance(node,Enemy)  and not node.visible or isinstance(node,Supply) and not node.visible:
                self.remove(node)
        #判断飞机与子弹的碰撞，判断飞机与飞机的碰撞
        self.collide()
        self.collide_flight()
        self.collide_supply()

    def collide(self):      #检测碰撞的函数
        # self.cm.clear()     #清空待检测区
        for node in self.get_children():       #寻找子节点并加入到待测区域中
            if isinstance(node,Bullet) and node.visible:
                bulletrect = node.get_rect()
                #得到敌机和子弹的交集
                for node2 in self.get_children():  # 获取当前层的所有子节点
                    if node.visible and isinstance(node2, Enemy):
                        enemyrect = node2.get_rect()
                        if bulletrect.intersect(enemyrect):
                            node.visible = False
                            self.remove(node)
                        #执行操作
                            node2.current_life -= 1
                            if node2.current_life <= 0:
                                self.score += node2.score
                                self.supply_score += node2.score
                                self.remove(self.label)
                                self.init_scorehub()
                                node2.visible = False
                                enemy_die = Enemy_die(node2.position,node2.type)
                                if node2.type == 1:
                                    Sound.play_effect("enemy1_down", Sound.effect_status)
                                if node2.type == 2:
                                    Sound.play_effect("enemy2_down", Sound.effect_status)
                                enemy_die.die_enemy()
                                self.add(enemy_die)
                                continue

    def collide_flight(self):  # 检测碰撞的函数
        for node2 in self.get_children():  # 获取当前层的所有子节点
            if node2.visible and isinstance(node2, Enemy):
                enemyrect = node2.get_rect()
                for node3 in self.get_children():  # 获取当前层的所有子节点
                    if isinstance(node3, Fight):
                        flightrect = node3.get_rect()
                        if flightrect.intersect(enemyrect):
                            # 执行操作
                            node3.life -= 1
                            node2.visible = False
                            self.remove(node2)
                            if node3.life == 2:
                                node3.visible = False
                                node3.position = 240,32
                                node3.visible = True
                                self.remove(self.life_img3)
                            elif node3.life == 1:
                                node3.visible = False
                                node3.position = 240, 32
                                node3.visible = True
                                self.remove(self.life_img2)
                            elif node3.life == 0:
                                File_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
                                config = configparser.ConfigParser()
                                config.read(File_Path + "/config.ini", encoding="utf-8")
                                judge_best_score = config.getint("setting", "best_score")
                                if judge_best_score < self.score:
                                    config.set("setting", "best_score", str(self.score))
                                    with open('config.ini', 'w+') as file:
                                        config.write(file)
                                director.pop()
                            else:
                                pass
                            continue

    def collide_supply(self):  # 检测碰撞的函数
        for node2 in self.get_children():  # 获取当前层的所有子节点
            if node2.visible and isinstance(node2, Supply):
                supplyrect = node2.get_rect()
                for node3 in self.get_children():  # 获取当前层的所有子节点
                    if isinstance(node3, Fight):
                        flightrect = node3.get_rect()
                        if flightrect.intersect(supplyrect):
                            # 执行操作
                            node2.visible = False
                            self.bullet_type = 2
                        else:
                            pass
                        continue




    def init_scorehub(self,score = None):
        score = self.score
        self.label = Label("Score:"+ str(score),
                     font_name="Kristen ITC",
                     font_size=22,
                     anchor_x="center",
                     anchor_y="center")

        # 得到屏幕尺寸和设置品目尺寸
        self.label.position = 400, 620
        # 把标签添加进层
        self.add(self.label,0)

    def init_lifehub(self):
        self.life_img1 = Sprite("life.png",scale= 0.5)
        self.life_img2 = Sprite("life.png",scale= 0.5)
        self.life_img3 = Sprite("life.png",scale= 0.5)
        self.life_img1.position = 20,25
        self.life_img2.position = 50,25
        self.life_img3.position = 80,25
        self.add(self.life_img1, 0)
        self.add(self.life_img2, 0)
        self.add(self.life_img3, 0)

    def init_statusbar(self):
        self.pause_button = Sprite("pause_nor.png")
        self.pause_button.position = 25,600
        self.add(self.pause_button,2)

        self.resume_button = Sprite("resume_nor.png")
        self.resume_button.position = 230,320
        self.add(self.resume_button,2)
        self.resume_button.visible = False

    def on_mouse_press(self,x,y,button,modifiers):
        if button == pyglet.window.mouse.LEFT:
            pause_button_rect = self.pause_button.get_rect()
            if pause_button_rect.contains(x,y) and self.pause_status == 0:
                self.resume_button.visible = True

                self.pause_button.visible = False
                self.pause_status = 1
                #暂停游戏
                for node2 in self.get_children():
                    if node2.visible and isinstance(node2, Enemy):
                        node2.pause_enemy()
                    if node2.visible and isinstance(node2, Bullet):
                        node2.pause_bullet()

        if button == pyglet.window.mouse.LEFT:
            resume_button_rect = self.resume_button.get_rect()
            if resume_button_rect.contains(x,y) and self.pause_status == 1:
                self.pause_button.visible = True

                self.resume_button.visible = False
                self.pause_status = 0
                #暂停游戏
                for node2 in self.get_children():
                    print(node2)
                    if node2.visible and isinstance(node2, Enemy):
                        node2.resume_enemy()
                    if node2.visible and isinstance(node2, Bullet):
                        node2.resume_bullet()

    def init_background(self):
        #初始化背景图
        sprite = Sprite("background.png")
        sprite.position = self.width // 2,self.height // 2
        self.add(sprite,0)



    def BG_music(self):
        #初始化背景音乐
        Sound.play_music(Sound.music_status)
        Sound.stop2(self.scene_status)

    def init_sprite_flight(self):
        #初始化飞机
        self.flight = Fight((0,0))
        self.flight.position = self.width // 2,self.flight.height // 2
        self.add(self.flight, 1)

    def init_sprite_enemy(self):
        #初始化敌人
        self.enemy = Enemy((0,0))
        self.enemy.position = self.width // 2,self.height + self.enemy.height//2
        self.enemy.shoot_enemy()
        self.add(self.enemy, 1)

    def init_sprite_supply(self):
        #初始化敌人
        self.supply = Supply((0,0))
        self.supply.position = self.width // 2,self.height + self.supply.height//2
        self.supply.shoot_supply()
        self.add(self.supply, 1)


    def init_sprite_bullet(self):
        #初始化子弹
        bullet2 = pyglet.image.load("./resources/image/bullet2.png")
        xx,yy  = self.flight.position
        type = self.bullet_type
        if self.bullet_type == 1:
            self.bullet = Bullet((xx,yy+self.flight.height//2),type)
            self.add(self.bullet,1)
            Sound.play_effect("bullet", Sound.effect_status)
        if  self.bullet_type == 2:
            print("2")
            self.bullet1 = Bullet((xx-20, yy + self.flight.height // 2),type)
            self.bullet1.image = bullet2
            self.add(self.bullet1, 1)
            print("add1")
            self.bullet2 = Bullet((xx+20, yy + self.flight.height // 2),type)
            self.bullet2.image = bullet2
            self.add(self.bullet2, 1)
            Sound.play_effect("bullet", Sound.effect_status)
            print("add2")

def create_background_scene():
    background_scene = Scene(Background())
    return background_scene

