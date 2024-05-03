"""----INSERT GAME NAME----

This module loads the mob data and creates the "Game" object. Finally it starts
the game.
"""

__version__ = "0.3"
__author__ = "Alex Page, Reuben Wiles Maguire"

import pgzero, pgzrun, pygame
from pgzero.builtins import keyboard, keys
from time import time
import math, sys, random
from enum import Enum
from game import Game
from constants import *
from csv import DictReader


if sys.version_info < (3,5):
    print("This game requires at least version 3.5 of Python. Please download\
          it from www.python.org")
    sys.exit()

pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_version < [1,2]:
    print("This game requires at least version 1.2 of Pygame Zero.\
You have version {0}. Please upgrade using the command 'pip3 install\
--upgrade pgzero'".format(pgzero.__version__))
    sys.exit()

class State(Enum):
    """Enum used to track the state of the game."""

    MENU = 1
    PLAY = 2
    GAME_OVER = 3
    PAUSE = 4
    LEVEL_UP = 5

def update():
    """Runs every game cycle. Checks the state of the game and either:
    - waits for the player to press space to start the game. (MENU)
    - runs the "update" method for "game" and check if the player character is
      dead or if the player has paused the game and records the time of the 
      pause. (PLAY)
    - waits for the player to press space to create a new game object. 
      (GAME_OVER)
    - waits for the player to press space to resume the game and calculates how
      long the game has been paused, then applies this offset to the game timer.
      (PAUSE)
    - TODO (LEVEL_UP)
    """

    global state, game, mobs, time_paused

    if state == State.MENU and keyboard.space:
        state = State.PLAY
        game.game_start_time = time()

    elif state == State.PLAY:
        if game.player.health <= 0:
            state = State.GAME_OVER

        elif keyboard.escape:
            time_paused = time()
            state = State.PAUSE
            game.update()

        else:
            game.update()
    
    elif state == State.GAME_OVER:
        if keyboard.space:
            state = State.MENU
            game = Game(mobs)

    elif state == State.PAUSE:
        if keyboard.space:
            time_diff = time() - time_paused
            game.game_start_time += time_diff
            state = State.PLAY

    elif state == State.LEVEL_UP:
        pass

def draw():
    """Runs every game cycle. Checks the state of the game and either:
    - shows the main menu. (MENU)
    - runs the "draw" function of "game". (PLAY)
    - shows the game over screen. (GAME_OVER)
    - shows the pause menu. (PAUSE)
    - shows the level up menu. (LEVEL_UP)
    """

    if state == State.MENU:
        pass
    elif state == State.PLAY:
        game.draw(screen)
    elif state == State.GAME_OVER:
        pass
    elif state == State.PAUSE:
        pass
    elif state == State.LEVEL_UP:
        pass

# Loads mob data from "mobs.csv"
with open("values/mobs.csv", "r") as file:
    reader = DictReader(file)
    mobs = []
    for row in reader:
        mobs.append(row)

    # Sets the data type for each entry
    for row in range(len(mobs)):
        mobs[row]["speed"] = int(mobs[row]["speed"])
        mobs[row]["health"] = int(mobs[row]["health"])
        mobs[row]["damage"] = int(mobs[row]["damage"])
        mobs[row]["spawn_time"] = list(map(int,
                                           mobs[row]["spawn_time"].split("/")))
        mobs[row]["xp_value"] = int(mobs[row]["xp_value"])

state = State.MENU
game = Game(mobs)
pgzrun.go()