from pygame import transform
from game_actors import Player, Monster
from constants import *


class Game():
    def __init__(self):
        self.player = Player("dragon_boss", HALF_LEVEL_W, HALF_LEVEL_H, 5, 100, "dragon_boss")
        self.monster = []

    def draw(self, screen):
        offset_x = self.player.x #max(0, min(LEVEL_W - WIDTH, self.player.x - WIDTH / 2))
        offset_y = self.player.y #max(0, min(LEVEL_H - HEIGHT, self.player.y - HEIGHT / 2))

        screen.blit("pitch", (-offset_x, -offset_y))

        #self.player._surf = transform.scale(self.player._surf, (300,300))
        self.player.draw(0, 0)

    def update(self):
        self.player.update()