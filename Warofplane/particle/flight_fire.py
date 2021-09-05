# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 0:27
# @Author  : Roy
# @Email   : yubr@qq.com
# @File    : flight_fire.py
# @Software: PyCharm


import cocos.particle_systems
from cocos.particle import Color


class FlightFire(cocos.particle_systems.Smoke):
    def __init__(self):
        super(FlightFire, self).__init__()
        self.angle = 270
        self.speed = 50.0
        self.life = 1.0
        self.size = 20.0
        self.duration = -1
        self.start_color = Color(0.5, 0.5, 0.5, 0.1)
        self.start_color_var = Color(0, 0, 0, 0.1)
        self.end_color = Color(0.5, 0.5, 0.5, 0.1)
        self.end_color_var = Color(0, 0, 0, 0.1)


class FlightEngine(cocos.particle_systems.Fire):
    def __init__(self):
        super(FlightEngine, self).__init__()
        self.angle = 270
        self.speed = 50.0
        self.life = 1.0
        self.duration = -1
