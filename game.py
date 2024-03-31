from pygame import transform
from game_actors import Player, Monster
from constants import *
from pygame.math import Vector2
from time import time


class Game():
    def __init__(self, mobs):
        self.player = Player("dragon_boss", HALF_LEVEL_W, HALF_LEVEL_H, 5, 100, "dragon_boss")
        self.mobs = mobs
        self.monster_alive = []
        self.game_start_time = time()
        self.current_time = 0.0
        self.current_minute = 0
        self.timer = 0

    def screen_coords(self):
        left = int(max(0, min(LEVEL_W - WIDTH, self.player.x_pos - WIDTH / 2)))
        top = int(max(0, min(LEVEL_H - HEIGHT, self.player.y_pos - HEIGHT / 2)))
        right = int(max(0, min(LEVEL_W + WIDTH, self.player.x_pos + WIDTH / 2)))
        bottom = int(max(0, min(LEVEL_H + HEIGHT, 
                                self.player.y_pos + HEIGHT / 2)))
        return (left, top, right, bottom)
    
    def update(self):
        self.current_time = time() - self.game_start_time
        self.current_minute = int(self.current_time // 60)

        self.player.update()

        self.timer += 1
        if self.timer == SPAWN_RATE:
            self.timer = 0
            for index, row in zip(range(len(self.mobs)), self.mobs):
                if (self.current_minute in row["spawn_time"] 
                    and not (row["has_spawned"] and row["unique"])):
                    self.mobs[index]["has_spawned"] = True
                    self.monster_alive.append(Monster(row["img"],
                                                      self.screen_coords(),
                                                      row["speed"],
                                                      row["health"],
                                                      row["damage"],
                                                      row["dir"]))
        for monster in self.monster_alive:
            if not monster.alive:
                self.monster_alive.remove(monster)
            monster.update(self.player)


    def draw(self, screen):
        offset_x = max(0, min(LEVEL_W - WIDTH, self.player.x_pos - WIDTH / 2))
        offset_y = max(0, min(LEVEL_H - HEIGHT, self.player.y_pos - HEIGHT / 2))

        screen.blit("pitch", (-offset_x, -offset_y))
        self.player.draw(offset_x, offset_y)

        for monster in self.monster_alive:
            monster.draw(offset_x, offset_y)