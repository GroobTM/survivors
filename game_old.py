import pgzero, pgzrun, pygame
import math, sys, random
from myactors import Player, Monster, Bat
from constants import *
from pygame.math import Vector2

class Game:
    def __init__(self):
        self.player = Player(HALF_LEVEL_W, HALF_LEVEL_H)
        self.monster = []
        self.timer = 0
        
    
    def draw(self,screen):
      offset_x = max(0, min(LEVEL_W - WIDTH, self.player.vposx - WIDTH / 2))
      offset_y = max(0, min(LEVEL_H - HEIGHT, self.player.vposy - HEIGHT / 2))
      offset = Vector2(offset_x, offset_y)

      screen.blit("pitch", (-offset_x, -offset_y))

      self.player.draw(offset_x, offset_y)
      for mob in self.monster:
        mob.draw(offset_x, offset_y)
    
    def update(self):
      self.player.update()

      self.timer += 1
      if (self.timer == 20):
        self.timer = 0
        self.monster.append(Bat(self.screencoords()))

      for mob in self.monster:
        mob.update(self.player)
        if (not mob.alive):
           self.monster.remove(mob)

    def screencoords(self):
      left = int(max(0, min(LEVEL_W - WIDTH, self.player.vposx - WIDTH / 2)))
      top = int(max(0, min(LEVEL_H - HEIGHT, self.player.vposy - HEIGHT / 2)))
      right = int(max(0, min(LEVEL_W + WIDTH, self.player.vposx + WIDTH / 2)))
      bottom = int(max(0, min(LEVEL_H + HEIGHT, self.player.vposy + HEIGHT / 2)))
      coords = [left, top, right, bottom]          
      return coords

