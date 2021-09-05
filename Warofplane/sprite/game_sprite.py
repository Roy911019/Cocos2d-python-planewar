# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 22:55
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : flight.py
# @Software: PyCharm
from collections import defaultdict
import pyglet

from particle.flight_fire import FlightFire
from cocos.director import director
from cocos.sprite import Sprite
from cocos.collision_model import AARectShape
from cocos.euclid import Vector2            #欧几里得导入矢量
from pyglet.window import key



# class Actor(Sprite):        #定义大体的演员类型，并进行矩形化
#     def __init__(self, image, pos):
#         super().__init__(image)
#         self.scale = 0.5
#         self.position = pos         #初始起始位置
#         # self.cshape = AARectShape(Vector2(self.x, self.y), self.width/2, self.height/2)    #参数为（cnter中心点和一半的宽和高）
#         # self.cshape = CircleShape(Vector2(self.x, self.y), self.width / 2)              #参数为（cnter中心点和半径人r），物体抽象为几何图形，
#         #待检测对象必须包含cshape属性
#
#     # def update_cshape(self):        #更新物体中心位置的变化
#     #     self.cshape.center = Vector2(self.x, self.y)

class Bullet(Sprite):
    def __init__(self, pos,type):
        super().__init__("bullet1.png",pos,type)
        self.position = pos         #初始起始位置
        self.direction = 4      #子弹飞行速度
        self.type = type
        # self.scale = 5
        self.window_width, self.window_height = director.get_window_size()

    def shoot_bullet(self,Node):  # 老鼠超过品目范围会调转方向,并更新老鼠的位置信息
        x,y = Node.position
        self.position = x , y+Node.height//2
        self.schedule(self.update)


    def shoot_bullet2(self,Node):  # 老鼠超过品目范围会调转方向,并更新老鼠的位置信息
        x,y = Node.position
        self.position = x-20 , y+Node.height//2
        self.schedule(self.update)
        print(x,y)


    def shoot_bullet3(self,Node):  # 老鼠超过品目范围会调转方向,并更新老鼠的位置信息
        x,y = Node.position
        self.position = x+20 , y+Node.height//2
        self.schedule(self.update)
        print(x,y)


    def update(self,dt):
        # if self.visible == False:
        #     self.unschedule(self.update)
        #     return          #可写可不写
        self.y += self.direction
        # self.update_cshape()
        #超过屏幕就设置子弹不可见，并取消子弹不断更新状态
        if self.y > self.window_height:
            self.visible = False
            self.unschedule(self.update)

    def pause_bullet(self):
        """暂停游戏"""
        self.pause_scheduler()

    def resume_bullet(self):
        """恢复游戏"""
        self.resume_scheduler()



class Fight(Sprite):
    def __init__(self, pos):
        super().__init__('me2.png', pos)
        self.scale = 0.5
        self.position = pos         #初始起始位置
        self.tft = FlightFire()
        self.tft.position = 0,-self.height//2
        self.add(self.tft,0)
        self.life = 3

    def move(self, pressed):        #如果按住方向键会改变bool值（pressed）
        width_half = self.width
        height_half = self.height
        window_width,window_height = director.get_window_size()
        #判断屏幕的范围，精灵都缩小至原来的一半，所以自身判断也许缩小一半
        if pressed[key.LEFT]:
            if self.x > width_half//2:
                self.x -= 3
        elif pressed[key.RIGHT]:
            if self.x < window_width-width_half//2:
                self.x += 3
        elif pressed[key.UP]:
            if self.y < window_height-height_half//2:
                self.y += 3
        elif pressed[key.DOWN]:
            if self.y > height_half//2:
                self.y -= 3

        # self.update_cshape()

    #
    # class Enemy(Actor):
    #     def __init__(self, pos):
    #         super().__init__('enemy1.png', pos)
    #         self.window_width, self.window_height = director.get_window_size()
    #         self.speed = 2      #子弹飞行速度
    #
    #     def shoot_enemy(self):  # 老鼠超过品目范围会调转方向,并更新老鼠的位置信息
    #         width = random.randint(self.width//2,self.window_width - self.width//2)
    #         self.position = width , self.window_height + self.height // 2
    #         self.schedule(self.update)
    #
    #     def update(self,dt):
    #         self.y -= self.speed
    #         self.update_cshape()
    #         #超过屏幕就设置子弹不可见，并取消子弹不断更新状态
    #         if self.y < 0:
    #             self.visible = False
    #             self.unschedule(self.update)

    # def on_key_press(self, k, _):   #判断是否按了相应的键
    #     self.pressed[k] = 1
    #
    # def on_key_release(self, k, _):
    #     self.pressed[k] = 0

    # def change(self,pressed):
    #     if self.pressed[key.LEFT]:
    #         image = pyglet.resource.image('me1.png')
    #         self.image = image
    #     else:
    #         image = pyglet.resource.image('me2.png')
    #         self.image = image
    #
    # def update(self, dt):
    #     self.change(self.pressed)
