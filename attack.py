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
from numpy import radians, sin, cos


def sign(num):
    """Converts a number into its corresponding sign (-1, 0, 1).

    Parameters
    ----------
    num : int/float     - a number

    Return
    ------
    int                 - -1, 0, or 1
    """
    if num < 0:
        num = -1
    elif num > 0:
        num = 1
    else:
        num = 0
    return num

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
    player_pos_old      - position of the player last update

    Methods
    -------
    collision()         - Detects and handles collisions between the weapon
                          and mobs.
    check_duration()    - Checks how long the weapon has been around and removes
                          it if its life exceeds the weapons duration.
    remove()            - Deletes the weapon.
    movement_calc() : [int, int] - Calculates how far the player has moved since
                          the last update.
    move()              - Moves the weapon by (dx,dy)*speed and runs 
                          "collision".
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
        self.player_pos_old = player_pos
        
    def collision(self):
        """Detects collisions between the weapon and mobs. Causes damage to mobs
        it collides with. Reduces pierce if applicable and calls "remove" if 
        pierce reaches 0.
        """

        collision_index = self.collidelist(mob_list) # From Actor
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

    def movement_calc(self):
        """Calculates how far the player has moved since the last update.

        Return
        ------
        [x, y] : [int, int] - difference between players last position and
                          current position
        """

        move = [player_pos[0] - self.player_pos_old[0],
                player_pos[1] - self.player_pos_old[1]]
        self.player_pos_old = player_pos
        return move
    
    def move(self, dx, dy, speed):
        """Moves the weapon by (dx,dy)*speed incrementally and runs 
        "collision" at each increment.
        """

        for i in range(speed):
            self.x += dx
            self.y += dy
            self.collision()
        

class Projectile(Weapon):
    """A class that describes weapons that move in a straight line.

    Child of "Weapon"

    Attributes
    ----------
    speed : int         - speed of the projectile

    Methods
    -------
    update()            - Runs every game update. Runs "move" and 
                          "check_duration".
    
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

    def update(self):
        """Runs every game update. Runs "move" and "check_duration"."""
        self.move(self.dx, self.dy, self.speed)
        self.check_duration()


class Stab(Projectile):
    """A class that describes projectiles that continually spawn from the player
    character.

    Child of "Projectile"

    Methods
    -------
    update()            - Runs every game update. Runs "movement_calc" and
                          offsets x and y. Then runs parents "update".
    
    Parent
    ------
    """
    __doc__ += super.__doc__

    def __init__(self, img, damage, duration, dx, dy, speed, pierce=-1):
        """Constructs all attributes for the Stab class.

        Parameters
        ----------
        img : str           - name of a png file in ./images used for sprite
        damage : int        - amount of damage dealt by the stab
        duration : float    - amount of time the stab exists for
        dx : float          - x component of unit vector
        dy : float          - y component of unit vector
        speed : int         - speed of the stab
        pierce : int        - number of mobs the stab can penetrate (optional)
        """
        super().__init__(img, damage, duration, dx, dy, speed, pierce)
    
    def update(self):
        """Runs every game update. Runs "movement_calc" to calculate the players
        movement and applies this movement with "move". Then runs parents 
        "update".
        """
        player_movement = self.movement_calc()
        self.move(player_movement[0], player_movement[1], 1)
        super().update()


class Aura(Weapon):
    """A class that describes auras that constantly follow the player.

    Child of "Weapon"

    Attributes
    ----------
    interval : float    - amount of time between aura activations

    Methods
    -------
    move()              - Moves the weapon by (dx,dy) and runs "collision" if
                          the time since the aura last activated exceded the 
                          interval.
    update()            - Runs every game update. Runs "movement_calc", "move",
                          and "check_duration".

    Parent
    ------
    """
    __doc__ += super.__doc__

    def __init__(self, img, damage, duration, interval):
        """Constructs all attributes for the Aura class.

        Parameters
        ----------
        img : str           - name of a png file in ./images used for sprite
        damage : int        - amount of damage dealt by the aura
        duration : float    - amount of time the aura exists for
        interval : float    - amount of time between aura activations
        """

        self.interval = interval
        self.last_activation = time() - interval # Forces attck on first update
        super().__init__(img, damage, duration, 0, 0, -1)
    
    def move(self, dx, dy):
        """Moves the weapon by (dx,dy) and runs "collision" if the time since
        the aura last activated exceded the interval.
        """

        self.x += dx
        self.y += dy
        if time() - self.last_activation >= self.interval:
            self.collision()
            self.last_activation = time()
    
    def update(self):
        """Runs every game update. Runs "movement_calc" to calculate the players
        movement and applies this movement with "move". Then runs 
        "check_duration".
        """

        player_movement = self.movement_calc()
        self.move(player_movement[0], player_movement[1])
        self.check_duration()


class Orbital(Weapon):
    """A class that describes orbitals that rotate around the player chracter.

    Child of Weapon

    Attributes
    ----------
    radius : int        - radius of the orbital
    speed  : int        - linear speed of the orbital
    angular_speed : float   - angular speed of the orbital
    cur_angle : float   - current angle of the orbital
    max_rotation : int  - max angle the orbital can rotate to
    starting_angle : int    - the starting angle of the orbital

    Methods
    -------
    rotate()            - Moves the orbital its "angular_speed" over incremental
                          steps and runs "collision" at each step.
    rotate_limit()      - Checks if the orbital has exceeded its "max_rotation"
                          and runs "remove" if it has.
    update()            - Runs every game update. Runs "movement_calc", "move",
                          "rotate", "rotate_limit" and "check_duration".

    Parent
    ------
    """
    __doc__ += super.__doc__

    def __init__(self, img, damage, duration, radius, speed, max_rotation,
                 starting_angle = 0):
        """Constructs all attributes for the Orbital class.

        Parameters
        ----------
        img : str           - name of a png file in ./images used for sprite
        damage : int        - amount of damage dealt by the orbital
        duration : float    - amount of time the orbital exists for
        radius : int        - radius of the orbital
        speed : int         - linear speed of the orbital
        max_rotation : int  - max angle the orbital can rotate to
        starting_angle : int    - the starting angle of the orbital (optional)
        """

        self.radius = radius
        self.speed = speed
        self.angular_speed = speed / radius
        self.max_rotation = max_rotation * sign(speed) + starting_angle
        self.cur_angle = starting_angle
        super().__init__(img, damage, duration, 0, 0, -1)

        # Attack does not originate from the player so a new starting position
        # needs to be set.
        self.x = radius*cos(radians(starting_angle))
        self.y = radius*sin(radians(starting_angle))

    def rotate(self):
        """Moves the orbital its "angular_speed" over incremental steps and runs
        "collision" at each step. The number of steps is dictated by "speed".
        """

        angle_step = self.angular_speed/self.speed
        for i in range(self.speed):
            self.cur_angle += angle_step
            self.x = self.radius*cos(radians(self.cur_angle))
            self.y = self.radius*sin(radians(self.cur_angle))
            self.collision()

    def rotate_limit(self):
        """Checks if the orbital has exceeded its "max_rotation" and runs 
        "remove" if it has.
        """
        if ((self.speed < 0 and self.max_rotation < self.cur_angle) or 
            (self.speed > 0 and self.max_rotation > self.cur_angle)):
            self.remove()

    def update(self):
        """Runs every game update. Runs "movement_calc" to calculate the players
        movement and applies this movement with "move". Then runs "rotate", 
        "rotate_limit", and "check_duration".
        """
        player_movement = self.movement_calc()
        self.move(player_movement[0], player_movement[1], 1)
        self.rotate()
        self.rotate_limit()
        self.check_duration()