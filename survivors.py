"""----INSERT GAME NAME----

This module loads the mob data and creates the "Game" object. Finally it starts
the game.
"""

__version__ = "0.2"
__author__ = "Alex Page, Reuben Wiles Maguire"

import pgzero, pgzrun, pygame
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

# Loads mob data from "mobs.csv"
with open("mobs.csv", "r") as file:
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
        mobs[row]["has_spawned"] = bool(int(mobs[row]["has_spawned"]))
        mobs[row]["unique"] = bool(int(mobs[row]["unique"]))

def update():
    game.update()

def draw():
    game.draw(screen)



game = Game(mobs)
pgzrun.go()