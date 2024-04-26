"""Weapon Framework

This module defines the weapon class which handles the loading of the stats of 
weapons and the spawning of attacks.
"""
__version__ = "0.3"
__author__ = "Reuben Wiles Maguire"

from csv import DictReader
from time import time
from random import choice
from attack import Attack, Aimed_Attack
from constants import ATTACK_DELAY

class Weapon():
    """This class describes the basic functionality of a weapon, its 
    progression, and how it attacks.

    Attributes
    ----------
    name : str              - the weapons name
    icon : str              - the name of an image file in ./images used for the
                              weapons icon
    progression : dict      - dictionary that describes how "speed", "damage",  
                              "duration", "pierce", "quantity", and "frequency"
                              change as the weapon levels up
    level : int             - the current level of the weapon
    level_cap : int         - the max level of the weapon
    max_level : bool        - if the weapon has reached its level cap or not
    timer : int             - counts how much time has passed since the weapon
                              last attacked
    attacks : [obj,...]     - a list of attacks that currently exist
    speed : int             - speed of the weapons attack
    damage : int            - damage dealt by the weapons attack
    duration : float        - amount of time the weapons attack exists for
    pierce : int            - number of enemies the weapons attacks can pierce
    quantity : int          - the number of attacks the weapon makes at once
    frequency : int         - how often the weapon makes an attack

    Methods
    -------
    load_progression(file_name) : dict  - Loads and returns progression stats
                              from a csv file in ./values/weapons. (Not called
                              by default.)
    set_weapon_stats()      - Sets "speed", "damage", "duration", "pierce", 
                              "quantity", and "frequency" based on "progression"
                              and "level".
    level_up_weapon()       - Increases the weapons level and calls 
                              "set_weapoon_stats" to update the weapons stats
                              for the new level.
    spawn_attack(player, mob_list)  - Dummy method.
    update(player, mob_list)    - Runs every game update. Checks the difference
                              between the current time and the start of the 
                              weapons attack cycle. If this difference exceeds 
                              the current "attack_interval" spawn an attack and 
                              increments "attack_interval_index".
                              Also runs the update methods of all objects in 
                              "attacks" and removes objects that no longer 
                              exist.
    draw(x_offset, y_offset)    - Runs every game update. Runs the draw method
                              for all objects in "attacks".
    """

    def __init__(self, name, icon, progression):
        """Constructs the Weapon class.

        Parameter
        ---------
        name : str              - the weapons name
        icon : str              - the name of an image file in ./images used for
                                  the weapons icon
        progression : dict      - dictionary that describes how "speed", 
                                  "damage", "duration", "pierce", "quantity", 
                                  and "frequency" change as the weapon levels up
        """

        self.name = name
        self.icon = icon
        self.progression = progression
        self.level = 1
        self.level_cap = len(self.progression)
        self.max_level = False
        self.starting_time = time()
        self.delay = ATTACK_DELAY
        self.attack_interval = []
        self.attack_interval_index = 0
        self.attacks = []

        self.set_weapon_stats()
        
        
        for i in range(self.quantity):
            self.attack_interval.append(self.delay)
        self.attack_interval.append(round(self.frequency - self.delay * self.quantity, 3))

    def load_progression(self, file_name):
        """Loads and returns progression stats from a csv file.

        Parameters
        ----------
        file_name : str         - the name of a file in ./values

        Return
        ------
        dict                    - a dictionary containing progression stats
        """

        with open("values/weapons/"+file_name, "r") as file:
            reader = DictReader(file)
            progression = {}
            counter = 1
            for row in reader:
                progression[counter] = row
                counter += 1
            
            return progression

    def set_weapon_stats(self):
        """Sets "speed", "damage", "duration", "pierce", "quantity", and 
        "frequency" based on "progression" and "level".
        """

        self.speed = int(self.progression[self.level]["speed"])
        self.damage = int(self.progression[self.level]["damage"])
        self.duration = float(self.progression[self.level]["duration"])
        self.pierce = int(self.progression[self.level]["pierce"])
        self.quantity = int(self.progression[self.level]["quantity"])
        self.frequency = float(self.progression[self.level]["frequency"])

    def level_up_weapon(self):
        """Increases the weapons level and calls "set_weapoon_stats" to update 
        the weapons stats for the new level. If the new level is equal to the
        level cap, "max_level" is set to True.
        """

        if self.level != self.level_cap:
            self.level += 1
            if self.level == self.level_cap:
                self.max_level = True
            self.set_weapon_stats()

    def spawn_attack(self, player, mob_list):
        """Dummy method. Will be replaced and used to handle attack spawning.
        
        Parameters
        ----------
        player : obj            - the player object
        mob_list : [obj,...]    - a list of monsters that currently exist
        """

        pass

    def update(self, player, mob_list):
        """Runs every game update. Checks the difference between the current
        time and the start of the weapons attack cycle. If this difference
        exceeds the current "attack_interval" spawn an attack and increments
        "attack_interval_index". When "attack_interval_index" reaches the end
        of "attack_interval", "attack_interval_index" cycle is reset to 0.
        
        Also runs the update methods of all objects in "attacks" and removes 
        objects that no longer exist.

        Parameters
        ----------
        player : obj            - the player object
        mob_list : [obj,...]    - a list of monsters that currently exist
        """

        if (time() - self.starting_time >= 
            self.attack_interval[self.attack_interval_index]):
            self.attack_interval_index += 1
            self.starting_time = time()

            if self.attack_interval_index < len(self.attack_interval):
                self.spawn_attack(player, mob_list)
            else:
                self.attack_interval_index = 0

        for attack in self.attacks:
            if not attack.exists:
                self.attacks.remove(attack)
            attack.update(mob_list)
    
    def draw(self, x_offset, y_offset):
        """Runs every game update. Runs the draw method for all objects in 
        "attacks".
        
        Parameters
        ----------
        offset_x : int          - offset for the screens real and virtual x 
                                  position
        offset_y : int          - offset for the screens real and virtual y 
                                  position
        """

        for attack in self.attacks:
            attack.draw(x_offset, y_offset)


class Thrown_Dagger(Weapon):
    """This class describes the Thrown Dagger weapon.
    
    Child of Weapon

    Attributes
    ----------
    img : str               - name of a png file used for the weapons attack 
                              sprite
    img_dir : str           - directory of the png file used for the weapons 
                              attack sprite

    Methods
    -------
    spawn_attack()          - Adds an instance of the "Attack" class to 
                              "attacks".

    Parent
    ------
    """
    __doc__ += Weapon.__doc__

    def __init__(self):
        """Constructs the Thrown_Dagger class."""

        name = "Thrown Dagger"
        icon = "xp1"
        progression = self.load_progression("thrown_dagger.csv")
        self.img = "thrown_dagger_"
        self.img_dir = "thrown_dagger"
        super().__init__(name, icon, progression)

    def spawn_attack(self, player, mob_list):
        """Adds an instance of the "Attack" class to "attacks"."""

        self.attacks.append(Attack(self.img, player, self.speed, self.damage, 
                                   self.duration, self.pierce, self.img_dir))
        
class Arrow(Weapon):
    """This class describes the Bow and Arrow weapon.

    Child of Weapon

    Attributes
    ----------
    img : str               - name of a png file used for the weapons attack 
                              sprite
    img_dir : str           - directory of the png file used for the weapons 
                              attack sprite

    Methods
    -------
    spawn_attack()          - Adds an instance of the "Aimed_Attack" class to 
                              "attacks".

    Parent
    ------
    """
    __doc__ += Weapon.__doc__

    def __init__(self):
        """Constructs the Arrow class."""

        name = "Bow and Arrow"
        icon = "xp2"
        progression = self.load_progression("arrow.csv")
        self.img = "xp2"
        self.img_dir = ""
        super().__init__(name, icon, progression)

    def spawn_attack(self, player, mob_list):
        """Adds an instance of the "Aimed_Attack" class to "attacks"."""

        self.attacks.append(Aimed_Attack(self.img, player, mob_list, self.speed,
                                         self.damage, self.duration, 
                                         self.pierce, self.img_dir))
        
class Magic_Missile(Weapon):
    """This class describes the Magic Missile weapon.

    Child of Weapon

    Attributes
    ----------
    progression : dict      - dictionary that describes how "speed", "damage",  
                              "duration", "pierce", "quantity", "frequency", and
                              "homing" change as the weapon levels up
    img : str               - name of a png file used for the weapons attack 
                              sprite
    img_dir : str           - directory of the png file used for the weapons 
                              attack sprite
    homing : bool           - if the weapons attacks home in on monsters

    Methods
    -------
    set_weapon_stats()      - Sets "speed", "damage", "duration", "pierce", 
                              "quantity", "frequency", and "homing" based on 
                              "progression" and "level".
    spawn_attack()          - Adds an instance of the "Aimed_Attack" class to 
                              "attacks".

    Parent
    ------
    """
    __doc__ += Weapon.__doc__

    def __init__(self):
        """Constructs the Magic_Missile class."""

        name = "Magic Missile"
        icon = "xp3"
        progression = self.load_progression("magic_missile.csv")
        self.img = ["magic_missile_1", "magic_missile_2"]
        self.img_dir = "magic_missile"
        super().__init__(name, icon, progression)

    def set_weapon_stats(self):
        """Runs parent then sets "homing" based on "progression" and "level".
        """

        super().set_weapon_stats()
        self.homing = bool(int(self.progression[self.level]["homing"]))

    def spawn_attack(self, player, mob_list):
        """Adds an instance of the "Aimed_Attack" class to "attacks"."""

        self.attacks.append(Aimed_Attack(choice(self.img), player, mob_list, 
                                         self.speed, self.damage, self.duration,
                                         self.pierce, self.homing, 
                                         self.img_dir))