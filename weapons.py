"""Weapon Attack Framework

This module creates the framework for weapon attacks as they appear and behave
in the game window. (Weapon is refers to bullets and slashes rather than guns 
and swords.)
"""

__version__ = "0.1"
__author__ = "Reuben Wiles Maguire"

from pgzero.builtins import Actor
from time import time
from globals import mob_list, player_pos


class Weapon(Actor):
    """A class to outline the basic properties of a weapon.

    Attributes
    ----------
    img : str           - name of a png file in ./images used for sprite
    x : int             - x coordinate of the sprite
    y : int             - y coordinate of the sprite
    damage : int        - amount of damage dealt by the weapon
    duration : float    - amount of time the weapon exists for
    dx : float          - x component of unit vector
    dy : float          - y component of unit vector
    pierce : int        - number of mobs the weapon can penetrate
    spawn_time : float  - time at which the weapon was spawned

    Methods
    -------
    collision()         - Detects and handles collisions between the weapon
                          and mobs.
    check_duration()    - Checks how long the weapon has been around and removes
                          it if its life exceeds the weapons duration.
    remove()            - Deletes the weapon.
    update()            - Runs every game update. Runs "collision" and 
                          "check_duration".
    """

    def __init__(self, img, damage, duration, dx, dy, pierce = -1):
        """Constructs all attributes for the Weapon class.

        Parameters
        ----------
        img : str           - name of a png file in ./images used for sprite
        damage : int        - amount of damage dealt by the weapon
        duration : float    - amount of time the weapon exists for
        dx : float          - x component of unit vector
        dy : float          - y component of unit vector
        pierce : int        - number of mobs the weapon can penetrate (optional)
        """
        super.__init__(img, tuple(player_pos))
        self.damage = damage
        self.duration = duration
        self.dx = dx
        self.dy = dy
        self.pierce = pierce # -1 means infinite

        self.spawn_time = time()
        
    def collision(self):
        """Detects collisions between the weapon and mobs. Causes damage to mobs
        it collides with. Reduces pierce if applicable and calls "remove" if 
        pierce reaches 0.
        """
        collision_index = super.collidelist(mob_list)
        if collision_index != -1:
            mob_list[collision_index].lose_health(self.damage)
            #### need to add a lose_health method to mobs
            if self.pierce != -1:
                self.pierce -= 1
                if self.pierce == 0:
                    self.remove()
    
    def check_duration(self):
        """Checks how long the weapon has existed and calls "remove" if it life 
        excedes the duration.
        """
        if time() - self.spawn_time >= self.duration:
            self.remove()

    def remove(self):
        """Deletes the weapon."""
        del self

    def update(self):
        """Runs every game update. Runs "collision" and "check_duration"."""
        self.collision()
        self.check_duration()
        

class Projectile(Weapon):
    """A class that describes weapons that move in a straight line.

    Child of "Weapon"

    Attributes
    ----------
    speed : int         - speed of the projectile

    Methods
    -------
    move()              - Moves the projectile by (dx,dy)*speed and
                          processes for collisions.
    update()            - Runs every game update. Runs "move" and 
                          "check_duration" from parent.
    
    Parent
    ------
    """
    __doc__ += super.__doc__

    def __init__(self, img, damage, duration, dx, dy, speed, pierce=-1):
        """Constructs all attributes for the Projectile class.

        Parameters
        ----------
        img : str           - name of a png file in ./images used for sprite
        damage : int        - amount of damage dealt by the projectile
        duration : float    - amount of time the projectile exists for
        dx : float          - x component of unit vector
        dy : float          - y component of unit vector
        speed : int         - speed of the projectile
        pierce : int        - number of mobs the projectile can penetrate 
                              (optional)
        """
        super().__init__(img, damage, duration, dx, dy, pierce)
        self.speed = speed

    def move(self):
        """Moves the projectile by (dx,dy)*speed incrementally and runs 
        "collision" from parent at each increment.
        """
        for i in range(self.speed):
            self.x += self.dx
            self.y += self.dy
            super().collision()

    def update(self):
        """Runs every game update. Runs "move" and "check_duration" from 
        parent.
        """
        self.move()
        super().check_duration()


class Slash(Projectile):
    """A class that describes projectiles that continually spawn from the player
    character.

    Child of "Projectile"

    Methods
    -------
    update()            - Runs every game update. Resets x and y to the players 
                          current x and y. Then runs parents "update".
    
    Parent
    ------
    """
    __doc__ += super.__doc__

    def __init__(self, img, damage, duration, dx, dy, speed, pierce=-1):
        """Constructs all attributes for the Slash class.

        Parameters
        ----------
        img : str           - name of a png file in ./images used for sprite
        damage : int        - amount of damage dealt by the slash
        duration : float    - amount of time the slash exists for
        dx : float          - x component of unit vector
        dy : float          - y component of unit vector
        speed : int         - speed of the slash
        pierce : int        - number of mobs the slash can penetrate (optional)
        """
        super().__init__(img, damage, duration, dx, dy, speed, pierce)
    
    def update(self):
        """Runs every game update. Resets x and y to the players current x 
        and y. Then runs parents "update".
        """
        self.x = player_pos[0]
        self.y = player_pos[1]
        super().update()