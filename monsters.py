import pyxel
import os
import random


class Monster(object):
    monster_database = []
    paused = False
    count = 0
    player_x = 0
    player_y = 0
    battle = False
    monster_id = 0

    def __init__(self, monster_id, x, y):
        try:  # load files in cx_freeze
            file = open(os.path.join(os.path.dirname(__file__)[:-16], 'monsters.txt'))
            for line in file:
                exec(f'self.monster_database.append({line})')
            file.close()
        except FileNotFoundError:  # load files in python
            file = open(os.path.join(os.path.dirname(__file__), 'monsters.txt'))
            for line in file:
                exec(f'self.monster_database.append({line})')
            file.close()

        self.instance_id = Monster.count
        self.animation_frame = 1
        self.animation_counter = 0
        self.walking_counter = 0
        self.walking_direction = 0
        self.hitbox_x = []
        self.hitbox_y = []
        self.ux = x
        self.uy = y
        self.u1 = Monster.monster_database[monster_id][1]
        self.v1 = Monster.monster_database[monster_id][2]
        self.u2 = Monster.monster_database[monster_id][3]
        self.v2 = Monster.monster_database[monster_id][4]
        self.mu = Monster.monster_database[monster_id][5]
        self.mv = Monster.monster_database[monster_id][6]
        self.hp = Monster.monster_database[monster_id][7]
        self.local_monster_id = monster_id
        print('monter_id = ', monster_id)
        Monster.count += 1

    def clear(self):
        self.ux = -100
        self.uy = -100

    def draw_monster(self):
        if not Monster.paused:

            self.hitbox_x = [self.ux-8, self.uy, self.ux + 15, self.uy + 7]
            self.hitbox_y = [self.ux, self.uy - 8, self.ux + 7, self.uy + 15]
            pyxel.rectb(self.hitbox_x[0], self.hitbox_x[1], self.hitbox_x[2], self.hitbox_x[3], 8)
            pyxel.rectb(self.hitbox_y[0], self.hitbox_y[1], self.hitbox_y[2], self.hitbox_y[3], 8)

            if self.animation_frame == 1:
                pyxel.blt(self.ux, self.uy, 0, self.u1, self.v1, 8, 8, 0)
            else:
                pyxel.blt(self.ux, self.uy, 0, self.u2, self.v2, 8, 8, 0)
            if self.animation_counter < 4:
                self.animation_counter += 1
            else:
                if self.animation_frame == 1:
                    self.animation_frame = 0
                else:
                    self.animation_frame = 1
                self.animation_counter = 0
        self.collision(self.hitbox_x, self.hitbox_y)

    def walk_monster(self):
        if not Monster.paused:
            if self.collision(self.hitbox_x, self.hitbox_y):
                self.clear()
                Monster.battle = True
                Monster.monster_id = self.local_monster_id
                print('Monster.monster_id = ', Monster.monster_id, self.local_monster_id)
            if self.walking_counter < 30:
                self.walking_counter += 1
            else:
                self.walking_direction = random.randint(0, 3)
                if self.walking_direction == 0:
                    if self.is_empty(self.ux, self.uy-8):
                        self.uy -= 8
                if self.walking_direction == 1:
                    if self.is_empty(self.ux+8, self.uy):
                        self.ux += 8
                if self.walking_direction == 2:
                    if self.is_empty(self.ux, self.uy+8):
                        self.uy += 8
                if self.walking_direction == 3:
                    if self.is_empty(self.ux-8, self.uy):
                        self.ux -= 8
                self.walking_counter = 0

    def is_empty(self, x, y):
        if pyxel.tilemap(0).get(x // 8, y // 8) == 0 or pyxel.tilemap(0).get(x // 8, y // 8) >= 32:
            return True
        else:
            return False

    def collision(self, hitbox_x, hitbox_y):
        hitbox_x_collision = [
            Monster.player_x+4 >= hitbox_x[0],
            Monster.player_y+4 >= hitbox_x[1],
            Monster.player_x+4 <= hitbox_x[2],
            Monster.player_y+4 <= hitbox_x[3],
        ]
        hitbox_y_collision = [
            Monster.player_x+4 >= hitbox_y[0],
            Monster.player_y+4 >= hitbox_y[1],
            Monster.player_x+4 <= hitbox_y[2],
            Monster.player_y+4 <= hitbox_y[3],
        ]
        col = any([all(hitbox_x_collision), all(hitbox_y_collision)])
        return col
