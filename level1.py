import pyxel
import random

from monsters import Monster


class Level1:

    def __init__(self):
        self.m0 = Monster(0, 80, 16)
        self.m1 = Monster(1, 112, 112)

    def draw_level(self):
        self.draw_map()
        self.m0.draw_monster()
        self.m0.walk_monster()
        self.m1.draw_monster()
        self.m1.walk_monster()

    def draw_map(self):
        x = 0
        y = 0
        tm = 0
        u = 0
        v = 0
        w = 16
        h = 16
        pyxel.bltm(x, y, tm, u, v, w, h)
