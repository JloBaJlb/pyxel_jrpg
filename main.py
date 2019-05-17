import pyxel
import os

from level1 import Level1
from monsters import Monster
from battle import Battle


class App:
    item_database = []
    paused = False

    def __init__(self):
        pyxel.init(128, 128, caption="WHAT THE ACTUALLY FUCK", fps=25)

        try:  # load files in cx_freeze
            pyxel.load(os.path.join(os.path.dirname(__file__)[:-16], 'my_resource.pyxel'))
            file = open(os.path.join(os.path.dirname(__file__)[:-16], 'items.txt'))
            for line in file:
                exec(f'self.item_database.append({line})')
            file.close()
        except FileNotFoundError:  # load files in python
            pyxel.load(os.path.join(os.path.dirname(__file__), 'my_resource.pyxel'))
            file = open(os.path.join(os.path.dirname(__file__), 'items.txt'))
            for line in file:
                exec(f'self.item_database.append({line})')
            file.close()
        self.player_damage = 4
        self.player_hp = 10
        pyxel.mouse(visible=True)
        self.battle = Battle()
        self.menu_opened = False
        self.player_direction = 0
        self.player_animation_frame = 1
        self.player_animation_frame_counter = 0
        self.x = 0
        self.y = 0
        self.sx = 56
        self.sy = 48
        self.level = Level1()
        self.battle_init = False
        # init inventory
        self.inventory = []
        # init game app
        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.mouse(True)
        Monster.paused = App.paused  # sending vars to "monster.py"
        Monster.player_x = self.sx
        Monster.player_y = self.sy
        if Monster.battle:
            if not self.battle_init:
                self.battle.monster_id = Monster.monster_id
                self.battle.player_hp = self.player_hp
                self.battle.player_dmg = self.player_damage
                self.battle.monster_hp = Monster.monster_database[self.battle.monster_id][7]
                self.battle.monster_dmg = Monster.monster_database[self.battle.monster_id][7]
                self.battle_init = True
                print('init')
            App.paused = True
        elif not Monster.battle and not self.menu_opened:
            if self.battle_init:
                self.player_hp = self.battle.player_hp
            App.paused = False
            self.battle_init = False
        # CONTROLS #
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if not App.paused:
            if pyxel.btn(pyxel.KEY_LEFT):
                self.player_direction = 1
                if self.is_empty(self.sx, self.sy + 1) and self.is_empty(self.sx, self.sy + 6):
                    self.sx = self.sx - 1
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.player_direction = 0
                if self.is_empty(self.sx + 7, self.sy + 1) and self.is_empty(self.sx + 7, self.sy + 6):
                    self.sx = self.sx + 1
            if pyxel.btn(pyxel.KEY_UP):
                self.player_direction = 2
                if self.is_empty(self.sx + 1, self.sy) and self.is_empty(self.sx + 6, self.sy):
                    self.sy = self.sy - 1
            if pyxel.btn(pyxel.KEY_DOWN):
                self.player_direction = 3
                if self.is_empty(self.sx + 1, self.sy + 8) and self.is_empty(self.sx + 6, self.sy + 8):
                    self.sy = self.sy + 1

        if pyxel.btnp(pyxel.KEY_E):
            if App.paused and not self.menu_opened:
                pass
            else:
                if not self.menu_opened:
                    App.paused = True
                    self.menu_opened = True
                else:
                    App.paused = False
                    self.menu_opened = False

        elif pyxel.btnp(pyxel.KEY_F):
            for item in self.item_database:
                if self.get_tile() == item[1]:
                    pyxel.tilemap(0).set((self.sx + 4) // 8, (self.sy + 4) // 8, 0)  # clear that tile
                    self.inventory.append(self.item_database.index(item))

    def draw(self):
        pyxel.cls(0)
        print(self.player_hp)
        self.level.draw_level()
        self.mouse_button()
        if Monster.battle:
            self.battle.draw()
        if not App.paused:
            self.draw_player()
        elif self.menu_opened:
            self.draw_menu()

    def draw_menu(self):
        pyxel.bltm(0, 0, 0, 0, 16, 16, 16, 0)
        pyxel.text(14, 16, 'INVENTORY:', 9)  # text
        for i in range(9):
            try:
                pyxel.text(14, (i*10)+26, self.item_database[self.inventory[i]][0], 15)
            except IndexError:
                break

    def mouse_button(self):
        if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
            self.sx = pyxel.mouse_x
            self.sy = pyxel.mouse_y
            tx = pyxel.mouse_x // 8
            ty = pyxel.mouse_y // 8
            self.x = tx
            self.y = ty
            print(tx*8, ty*8, pyxel.tilemap(0).get(tx, ty))

    def draw_player(self):
        going = [
            pyxel.btn(pyxel.KEY_LEFT),
            pyxel.btn(pyxel.KEY_RIGHT),
            pyxel.btn(pyxel.KEY_UP),
            pyxel.btn(pyxel.KEY_DOWN)
        ]
        if any(going):
            self.player_cycle_animation()
        pyxel.blt(self.sx, self.sy, 0, self.player_direction*8, self.player_animation_frame*8, 8, 8, 0)

    def is_empty(self, x, y):
        if pyxel.tilemap(0).get(x // 8, y // 8) == 0 or pyxel.tilemap(0).get(x // 8, y // 8) >= 32:
            return True
        else:
            return False

    def get_tile(self):
        return pyxel.tilemap(0).get((self.sx+4) // 8, (self.sy+4) // 8)

    def player_cycle_animation(self):
        if self.player_animation_frame_counter < 4:
            self.player_animation_frame_counter += 1
        else:
            if self.player_animation_frame == 1:
                self.player_animation_frame = 2
                self.player_animation_frame_counter = 0
            else:
                self.player_animation_frame = 1
                self.player_animation_frame_counter = 0
