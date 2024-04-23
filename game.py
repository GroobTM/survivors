"""Game Class

This module defines the Game class. This class combines all other classes into
one place and describes how they communicate with each other.
"""
__version__ = "0.2"
__author__ = "Alex Page, Reuben Wiles Maguire"

from pygame import transform
from game_actors import Player, Monster
from constants import *
from time import time
from weapons import Thrown_Dagger, Arrow, Magic_Missile



class Game():
    """A class that describes the game and how objects communicate with each
    other.

    Attributes
    ----------
    player : obj        - the Player object
    mobs : [dict,...]   - a list of dictionaries that contain mob data
    monsters_alive : [obj,...]  - a list of Monster objects
    game_start_time : float - time the game started
    current_time : float    - amount of time thats passed since the game started
    current_minute : int    - number of minutes that have passed since the game
                              started.
    timer : int         - amount of game updates since the last monster spawned

    Methods
    -------
    screen_coords() : (int, int, int, int)  - Calculates the coordinates of the
                          edge of the screen.
    update()            - Runs every game update. Calculates the current time
                          and current minute. Adds new mobs to "monsters_alive"
                          and removes dead mobs from "monsters_alive".
                          Then, runs "update" for "player" and for each monster
                          in "monsters_alive".
    draw(screen)        - Calculates the position of the screen. Draws the 
                          background and calls the "draw" for "player" and each 
                          monster in "mosters_alive".
    """

    def __init__(self, mobs):
        """Constructs the Game class.

        Attributes
        ----------
        mobs : [dict,...]   - a list of dictionaries that contain mob data
        """

        self.player = Player("bat", HALF_LEVEL_W, HALF_LEVEL_H, 5, 100, "bat")
        self.mobs = mobs
        self.monsters_alive = []
        self.weapons = [Thrown_Dagger(), Arrow(), Magic_Missile()]
        self.game_start_time = time()
        self.current_time = 0.0
        self.current_minute = 0
        self.timer = 0

    def screen_coords(self):
        """Calculates the coordinates of the edge of the screen.

        Return
        ------
        (int, int, int, int)    - Position of the left, top, right, bottom of
                                  the screen.
        """
        
        left = int(max(0, min(LEVEL_W - WIDTH, self.player.x_pos - WIDTH / 2)))
        top = int(max(0, min(LEVEL_H - HEIGHT, self.player.y_pos - HEIGHT / 2)))
        right = int(max(0, min(LEVEL_W + WIDTH, self.player.x_pos + WIDTH / 2)))
        bottom = int(max(0, min(LEVEL_H + HEIGHT, 
                                self.player.y_pos + HEIGHT / 2)))
        return (left, top, right, bottom)
    
    def update(self):
        """Runs every game update. Calculates the current time and current 
        minute. 
        
        Checks how many updates have passed since the last batch of monsters
        spawned and, if enough have passed, adds a new batch to "monsters_alive"
        using data from "mobs".
        
        Removes monsters from "monsters_alive" if their "alive" attribute is 
        False.
        
        Then, runs "update" for "player" and for each monster in 
        "monsters_alive".
        """

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
                    self.monsters_alive.append(Monster(row["img"],
                                                      self.screen_coords(),
                                                      row["speed"],
                                                      row["health"],
                                                      row["damage"],
                                                      row["dir"]))
        
        for monster in self.monsters_alive:
            if not monster.alive:
                self.monsters_alive.remove(monster)
            monster.update(self.player)
        for weapon in self.weapons:
            weapon.update(self.player, self.monsters_alive)


    def draw(self, screen):
        """Calculates the position of the screen. Draws the background and calls
        the "draw" for "player" and each monster in "mosters_alive".
        """

        offset_x = max(0, min(LEVEL_W - WIDTH, self.player.x_pos - WIDTH / 2))
        offset_y = max(0, min(LEVEL_H - HEIGHT, self.player.y_pos - HEIGHT / 2))

        screen.blit("pitch", (-offset_x, -offset_y))
        self.player.draw(offset_x, offset_y)
        for monster in self.monsters_alive:
            monster.draw(offset_x, offset_y)
        for weapon in self.weapons:
            weapon.draw(offset_x, offset_y)