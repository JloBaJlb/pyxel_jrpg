import pyxel
import random

from monsters import Monster


class Battle:

    def __init__(self):
        self.monster_id = 0
        self.i = 0
        self.frame = 0
        self.battle_frame = 0
        self.attack = False
        self.dmg = 0
        self.end_anim = False

        self.player_x = 100
        self.player_y = 100
        self.player_hp = 0
        self.player_dmg = 0

        self.monster_x = 10
        self.monster_y = 100
        self.monster_hp = 0
        self.monster_dmg = 0

    def draw(self):
        #  MAIN TIMELINE  #
        print('Monster Id ', self.monster_id,
              'Monster Dmg ', self.monster_dmg,
              'Monster Hp ', self.monster_hp,
              'Player Hp ', self.player_hp,
              'Player Dmg', self.player_dmg,
              'Frame', self.frame)
        if self.frame < 32:  # clothing game window
            self.i += 2
            pyxel.clip(self.i, self.i, 128 - self.i, 128 - self.i)
            self.frame += 1
        elif self.frame < 64:  # opening game window
            pyxel.bltm(0, 0, 0, 16, 16, 16, 16)
            self.i += 2
            pyxel.clip(self.i, self.i, 128 - self.i, 128 - self.i)
            self.draw_sprites()
            self.frame += 1
        else:              # infinity
            pyxel.bltm(0, 0, 0, 16, 16, 16, 16)
            pyxel.clip()
            self.monster_dmg = Monster.monster_database[self.monster_id][8]
            self.draw_sprites()
            if not self.end_anim:
                self.player_hit_anim()
            if pyxel.btn(pyxel.KEY_T):
                self.frame = 0
                self.battle_frame = 0
                self.i = 0
                self.end_anim = False
                Monster.battle = False
        if self.end_anim:
            if self.frame == 64:
                self.i = 0
            if self.frame < 97:
                pyxel.rect(0, 0, 128, self.i, 0)
                self.i += 4
                self.frame += 1
            else:
                self.attack = False
                self.player_x = 100
                self.frame = 0
                self.battle_frame = 0
                self.i = 0
                self.end_anim = False
                Monster.battle = False
        #  MAIN TIMELINE  #

    def draw_sprites(self):
        pyxel.blt(self.player_x, self.player_y, 0, 0, 56, 16, 16, 0)

        pyxel.blt(self.monster_x,
                  self.monster_y,
                  0,
                  Monster.monster_database[self.monster_id][5],
                  Monster.monster_database[self.monster_id][6],
                  16, 16, 0)

    def player_hit_anim(self):
        self.draw_hp_bara()
        if self.player_hp <= 0:
            pyxel.quit()
        if self.monster_hp <= 0:
            self.end_anim = True
        if not self.end_anim:
            if pyxel.btn(pyxel.KEY_ENTER):
                self.attack = True
        if self.attack:
            if self.battle_frame < 10:
                self.player_x -= 6
                self.battle_frame += 1
            elif self.battle_frame == 10:
                self.attack_mechanic(True)
                self.battle_frame += 1
            elif self.battle_frame < 21:
                pyxel.text(self.monster_x, self.monster_y - 10 - self.battle_frame, f'-{self.dmg}', 8)
                self.player_x += 6
                self.battle_frame += 1
            elif self.battle_frame < 31:
                self.monster_x += 6
                self.battle_frame += 1
            elif self.battle_frame == 31:
                self.attack_mechanic(False)
                self.battle_frame += 1
            elif self.battle_frame < 42:
                pyxel.text(self.player_x, self.player_y + 12 - self.battle_frame, f'-{self.dmg}', 8)
                self.monster_x -= 6
                self.battle_frame += 1
            elif self.battle_frame == 42:
                self.battle_frame = 0
                self.attack = False

    def attack_mechanic(self, is_player):
        if is_player:
            self.dmg = self.player_dmg + random.randint(-1, 1)
            self.monster_hp -= self.dmg
        else:
            self.dmg = self.monster_dmg + random.randint(-1, 1)
            self.player_hp -= self.dmg

    def draw_hp_bara(self):
        pyxel.blt(self.player_x, self.player_y-3, 0, 24, 32, 16, 3, 0)
        pyxel.blt(self.player_x+1, self.player_y-2, 0, 25, 36, int(14/10*self.player_hp), 1, 0)

        pyxel.blt(self.monster_x, self.monster_y - 3, 0, 24, 32, 16, 3, 0)
        pyxel.blt(self.monster_x + 1, self.monster_y - 2, 0, 25, 36, int(14 / 10 * self.monster_hp), 1, 0)