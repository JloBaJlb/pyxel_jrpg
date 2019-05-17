import pyxel
import random

from monsters import Monster


class Battle:
    anim_frame = 0
    anim_frame_sprites = 0
    anim_frame_hint_window = 0
    attack = False
    attack_dir = 0
    anim_hit_frame = 0
    player_damage = 0

    def __init__(self, monster_id):
        self.id = monster_id
        self.player_x = 138
        self.player_y = 100
        self.monster_x = -18
        self.monster_y = 100
        self.player_hp = 10
        self.monster_hp = 0
        self.dmg = 0
        self.enemy_turn = False
        self.monster_damage = 0
        self.monster_attack_dir = 0
        self.messeage_shown = False

    def draw(self):

        if Battle.anim_frame <= 64:
            self.closing_anim(Battle.anim_frame)  # closing anim
            Battle.anim_frame += 1

        else:
            self.init_scene()                     # drawing bg

        if Battle.anim_frame <= 128:
            self.opening_anim(Battle.anim_frame)  # opening anim
            Battle.anim_frame += 1

        elif Battle.anim_frame == 129:
            pyxel.clip()                          # fully opening anim
            self.sprite_draw(Battle.anim_frame_sprites)
            if Battle.anim_frame_sprites <= 26:
                Battle.anim_frame_sprites += 1
                self.monster_x = -16 + Battle.anim_frame_sprites
                self.player_x = 128 - Battle.anim_frame_sprites                # drawing sprites
        if Battle.anim_frame_sprites == 27:
            if not self.messeage_shown:
                self.draw_hint_window(Battle.anim_frame_hint_window)   # draw hint window
            if Battle.anim_frame_hint_window <= 55:
                Battle.anim_frame_hint_window += 1
        if Battle.anim_frame_hint_window == 56:       # fight
            if not self.messeage_shown:
                pyxel.text(9, 21, 'To attack choose attack di-', 7)
                pyxel.text(9, 31, 'rection with up and down', 7)
                pyxel.text(9, 41, 'arrows          <ENTER>', 7)
                if pyxel.btn(pyxel.KEY_ENTER):
                    self.messeage_shown = True
            if pyxel.btn(pyxel.KEY_UP):
                Battle.attack = True
                Battle.attack_dir = 1
            elif pyxel.btn(pyxel.KEY_DOWN):
                Battle.attack = True
                Battle.attack_dir = 0

            self.draw_hp_bars()
            if Battle.attack:
                self.attack_anim(Battle.anim_hit_frame)
                self.sprite_draw(Battle.anim_frame_sprites)
                if Battle.anim_hit_frame <= 60:  # battle anim
                    Battle.anim_hit_frame += 1

    def closing_anim(self, i):
        pyxel.clip(i, i, 128-i, 128-i)

    def init_scene(self):
        pyxel.bltm(0, 0, 0, 16, 16, 16, 16)

    def opening_anim(self, i):
        pyxel.clip(128-i, 128-i, i, i)

    def sprite_draw(self, i):
        pyxel.blt(self.player_x, self.player_y, 0, 0, 56, 16, 16, 0)
        pyxel.blt(self.monster_x, self.monster_y, 0, Monster.monster_database[self.id][5], Monster.monster_database[self.id][6], 16, 16, 0)

    def draw_hint_window(self, i):
        pyxel.rect(64-i, 19, 64+i, 20, 9)  # yellow top frame
        pyxel.rect(64-i, 20, 64+i, 50, 1)  # center
        pyxel.rect(64-i, 50, 64+i, 50, 9)  # yellow bottom frame
        if Battle.anim_frame_hint_window == 56:
            pyxel.rect(63 - i, 20, 63 - i, 49, 9)  # yellow side frame
            pyxel.rect(65 + i, 20, 65 + i, 49, 9)

    def attack_anim(self, i):
        if self.player_hp <= 0:
            pyxel.quit()
        elif self.monster_hp <= 0:
            Monster.battle = False

        if not self.enemy_turn:
            enemy_defence = random.randint(0, 1)
            if i < 10:  # first phase
                if i == 0:
                    self.monster_hp = Monster.monster_database[self.id][7]
                    self.monster_damage = Monster.monster_database[self.id][8]
                if self.attack_dir == 0:
                    self.player_x -= 1
                    self.player_y += 1
                else:
                    self.player_x -= 1
                    self.player_y -= 1
            elif i < 30:
                self.player_x -= 3
            elif i == 30:
                pyxel.play(0, 2)
                if Battle.attack_dir != enemy_defence:
                    self.dmg = self.player_damage + random.randint(-1, 1)
                    self.monster_hp -= self.dmg
                else:
                    self.dmg = 0
            elif i < 51:
                pyxel.text(16, 120-i, f'-{self.dmg}', 8)
                self.player_x += 3
            elif i < 60:
                if self.attack_dir == 0:
                    self.player_x += 1
                    self.player_y -= 1
                else:
                    self.player_x += 1
                    self.player_y += 1
            elif i == 60:
                self.enemy_turn = True
                Battle.anim_hit_frame = 0
        else:
            if i < 10:  # first phase
                if i == 1:
                    self.monster_attack_dir = random.randint(0, 1)
                    print(self.monster_attack_dir)
                if self.monster_attack_dir == 0:
                    self.monster_x += 1
                    self.monster_y += 1
                else:
                    self.monster_x += 1
                    self.monster_y -= 1
            elif i < 30:
                self.monster_x += 3
            elif i == 30:
                pyxel.play(0, 1)
                if self.monster_attack_dir != self.attack_dir:
                    self.dmg = self.monster_damage + random.randint(-1, 1)
                    self.player_hp -= self.dmg
                else:
                    self.dmg = 0
            elif i < 51:
                pyxel.text(110, 120 - i, f'-{self.dmg}', 8)
                self.monster_x -= 3
            elif i < 60:
                if self.monster_attack_dir == 0:
                    self.monster_x -= 1
                    self.monster_y -= 1
                else:
                    self.monster_x -= 1
                    self.monster_y += 1
            elif i == 60:
                Battle.attack = False
                self.enemy_turn = False
                Battle.anim_hit_frame = 0

    def draw_hp_bars(self):
        pyxel.blt(self.player_x, self.player_y-3, 0, 24, 32, 16, 3)
        pyxel.blt(self.player_x+1, self.player_y-2, 0, 25, 36, int(14/10*self.player_hp), 1, 0)

        pyxel.blt(self.monster_x, self.monster_y - 3, 0, 24, 32, 16, 3)
        pyxel.blt(self.monster_x + 1, self.monster_y - 2, 0, 25, 36, int(14 / 10 * self.monster_hp), 1, 0)
