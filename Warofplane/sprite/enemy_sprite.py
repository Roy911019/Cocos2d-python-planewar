# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 15:17
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : enemy_sprite.py
# @Software: PyCharm


# -*- coding: utf-8 -*-
# @Time    : 2021/8/29 22:55
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : flight.py
# @Software: PyCharm

import pyglet
from cocos.director import director
from cocos.sprite import Sprite
from cocos.collision_model import AARectShape
from cocos.euclid import Vector2            #欧几里得导入矢量
import random
import enum



class Enemy_type(enum.Enum):
    Enemy1 = 1  #小飞机
    Enemy2 = 2  #大飞机


enemylife = {Enemy_type.Enemy1 : 3,
              Enemy_type.Enemy2 : 6
}

enemyscore = {Enemy_type.Enemy1 : 1,
              Enemy_type.Enemy2 : 2
}

enemyspeed = {Enemy_type.Enemy1 : 1.5,
              Enemy_type.Enemy2 : 1
}

enemyimg = {Enemy_type.Enemy1 : 'enemy1.png',
              Enemy_type.Enemy2 : 'enemy2.png'
}

frame_seq1 = [pyglet.image.load("./resources/image/enemy1_down1.png"),pyglet.image.load("./resources/image/enemy1_down2.png"),
            pyglet.image.load("./resources/image/enemy1_down3.png"),pyglet.image.load("./resources/image/enemy1_down4.png"),
              pyglet.image.load("./resources/image/blank.png")]
frame_seq2 = [pyglet.image.load("./resources/image/enemy2_down1.png"),pyglet.image.load("./resources/image/enemy2_down2.png"),
              pyglet.image.load("./resources/image/enemy2_down3.png"),pyglet.image.load("./resources/image/enemy2_down4.png"),
              pyglet.image.load("./resources/image/blank.png")]
anim1 = pyglet.image.Animation.from_image_sequence(frame_seq1, 0.1,loop = False)
anim2 = pyglet.image.Animation.from_image_sequence(frame_seq2, 0.1,loop = False)
enemy_seq = {Enemy_type.Enemy1 : anim1,
              Enemy_type.Enemy2 :anim2
}

class Enemy_die(Sprite):
    def __init__(self,pos,type):
        super().__init__('enemy1.png', pos,type)
        self.position = pos         #初始起始位置
        self.type = type

    def die_enemy(self):
        if self.type ==  1:
            self.image = anim1
            print("更新图片")
        if self.type == 2 :
            self.image = anim2

class Enemy(Sprite):
    def __init__(self, pos):
        super().__init__('enemy1.png', pos)
        # self.scale = 0.5
        self.position = pos         #初始起始位置
        #初始化敌人信息
        self.type = random.randint(1,2)
        if self.type == 1:
            self.image = pyglet.resource.image(enemyimg[Enemy_type.Enemy1])
            self.initial_life = enemylife[Enemy_type.Enemy1]
            self.current_life = self.initial_life
            self.speed = enemyspeed[Enemy_type.Enemy1]
            self.score = enemyscore[Enemy_type.Enemy1]
        if self.type == 2:
            self.image = pyglet.resource.image(enemyimg[Enemy_type.Enemy2])
            self.initial_life = enemylife[Enemy_type.Enemy2]
            self.current_life = self.initial_life
            self.speed = enemyspeed[Enemy_type.Enemy2]
            self.score = enemyscore[Enemy_type.Enemy2]
        self.window_width, self.window_height = director.get_window_size()
        self.schedule(self.update)


    def shoot_enemy(self):  # 敌人开始行动
        width = random.randint(self.width//2,self.window_width - self.width//2)
        self.position = width , self.window_height + self.height // 2


    def pause_enemy(self):
        """暂停游戏"""
        self.pause_scheduler()

    def resume_enemy(self):
        """恢复游戏"""
        self.resume_scheduler()

    def update(self,dt):
        self.y -= self.speed
        # self.update_cshape()
        #超过屏幕就设置子弹不可见，并取消子弹不断更新状态
        if self.y < 0:
            self.visible = False
            self.unschedule(self.update)



class Supply(Sprite):
    def __init__(self, pos):
        super().__init__('bullet_supply.png', pos)
        # self.scale = 0.5
        self.position = pos         #初始起始位置
        self.speed = 1
        self.window_width, self.window_height = director.get_window_size()
        self.schedule(self.update)


    def shoot_supply(self):  # 敌人开始行动
        width = random.randint(self.width//2,self.window_width - self.width//2)
        self.position = width , self.window_height + self.height // 2

    def shoot_supply(self):
        """暂停游戏"""
        self.pause_scheduler()

    def shoot_supply(self):
        """恢复游戏"""
        self.resume_scheduler()

    def update(self,dt):
        self.y -= self.speed
        # self.update_cshape()
        #超过屏幕就设置子弹不可见，并取消子弹不断更新状态
        if self.y < 0:
            self.visible = False
            self.unschedule(self.update)
