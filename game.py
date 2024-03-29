from pygame import transform
from game_actors import Player, Monster
from constants import *
from pygame.math import Vector2


class Game():
    def __init__(self):
        self.player = Player("dragon_boss", HALF_LEVEL_W, HALF_LEVEL_H, 5, 100, "dragon_boss")
        self.monster = []

    def draw(self, screen):
        offset_x = max(0, min(LEVEL_W - WIDTH, self.player.x_pos - WIDTH / 2))
        offset_y = max(0, min(LEVEL_H - HEIGHT, self.player.y_pos - HEIGHT / 2))

        screen.blit("pitch", (-offset_x, -offset_y))
        #self.player._surf = transform.scale(self.player._surf, (300,300))
        self.player.draw(offset_x, offset_y)


    def update(self):
        self.player.update()