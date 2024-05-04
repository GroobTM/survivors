"""Game

This module defines the Game class. This class combines all other classes into
one place and describes how they communicate with each other.
"""
__version__ = "0.6"
__author__ = "Alex Page, Reuben Wiles Maguire"

from pygame import transform
from time import time
from random import randint
from game_actors import Player, Monster
from collectables import XP, Cake
from weapons import Thrown_Dagger, Arrow, Magic_Missile
from constants import *


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
    xp : int            - current player xp
    xp_cap : int        - xp required to level up

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

        self.player = Player("princess", HALF_LEVEL_W, HALF_LEVEL_H, 
                             5, 100, "princess")
        self.mobs = mobs
        self.monsters_alive = []
        self.collectables = []
        self.weapons = [Magic_Missile(), Thrown_Dagger()]
        self.game_start_time = time()
        self.current_time = 0.0
        self.current_minute = 0
        self.timer = 0
        self.xp = 0
        self.xp_cap = LEVEL_CAP_BASE
        self.level = 1

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
                if (self.current_minute in row["spawn_time"] ):
                    self.monsters_alive.append(Monster(row["img"],
                                                      self.screen_coords(),
                                                      row["speed"],
                                                      row["health"],
                                                      row["damage"],
                                                      row["xp_value"],
                                                      row["dir"]))
        
        for monster in self.monsters_alive:
            if not monster.alive:
                if monster.damage_death:
                    self.collectables.append(XP(monster))
                    if randint(1, 100) <= HEAL_SPAWN_CHANCE:
                        self.collectables.append(Cake(monster))
                self.monsters_alive.remove(monster)
            monster.update(self.player)
        for collectable in self.collectables:
            if not collectable.exists:
                self.collectables.remove(collectable)
            collectable.update(self)
        for weapon in self.weapons:
            weapon.update(self.player, self.monsters_alive)


    def draw(self, screen):
        """Calculates the position of the screen. Draws the background and calls
        the "draw" for "player" and each monster in "mosters_alive".
        """

        offset_x = max(0, min(LEVEL_W - WIDTH, self.player.x_pos - WIDTH / 2))
        offset_y = max(0, min(LEVEL_H - HEIGHT, self.player.y_pos - HEIGHT / 2))

        screen.blit("background", (-offset_x, -offset_y))
        self.player.draw(offset_x, offset_y)
        for collectable in self.collectables:
            collectable.draw(offset_x, offset_y)
        for monster in self.monsters_alive:
            monster.draw(offset_x, offset_y)
        for weapon in self.weapons:
            weapon.draw(offset_x, offset_y)
        
        # GUI
        xp_offset = max(0, (1 - self.xp / self.xp_cap) * WIDTH)
        screen.blit("gui\\gui_xp_bar", (-xp_offset + BAR_BORDER, BAR_BORDER))

        hp_offset = min((1 - self.player.health / self.player.max_health) * 
                        WIDTH, WIDTH)
        screen.blit("gui\\gui_health_bar", (-hp_offset + BAR_BORDER, 
                                       HEIGHT - BAR_HEIGHT + BAR_BORDER))

        screen.blit("gui\\gui_box", (0, 0))
        screen.blit("gui\\gui_box", (0, HEIGHT - BAR_HEIGHT))

        if self.level >= 10:
            tens, digits = list(str(self.level))
        else:
            tens, digits = ["0", str(self.level)]
        screen.blit("numbers\\"+tens, (HALF_WINDOW_W - HALF_NUMBER_GAP - 
                                   NUMBER_WIDTH, 0))
        screen.blit("numbers\\"+digits, (HALF_WINDOW_W + HALF_NUMBER_GAP, 0))

        minutes, seconds = divmod(int(self.current_time), 60)
        if seconds >= 10:
            sec_tens, sec_digits = list(str(seconds))
        else:
            sec_tens, sec_digits = ["0", str(seconds)]
            
        if minutes >= 10:
            min_tens, min_digits = list(str(minutes))
        else:
            min_tens, min_digits = ["0", str(minutes)]
        screen.blit(f"numbers\\{sec_digits}_black", 
                    (WIDTH - TIMER_SEPARATION, NUMBER_HEIGHT + NUMBER_GAP))
        screen.blit(f"numbers\\{sec_tens}_black", 
                    (WIDTH - 2 * TIMER_SEPARATION, NUMBER_HEIGHT + NUMBER_GAP))
        screen.blit("numbers\\colon_black", 
                    (WIDTH - 3 * TIMER_SEPARATION, NUMBER_HEIGHT + NUMBER_GAP))
        screen.blit(f"numbers\\{min_digits}_black",
                    (WIDTH - 4 * TIMER_SEPARATION, NUMBER_HEIGHT + NUMBER_GAP))
        screen.blit(f"numbers\\{min_tens}_black", 
                    (WIDTH - 5 * TIMER_SEPARATION, NUMBER_HEIGHT + NUMBER_GAP))
        
