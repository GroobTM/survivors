"""Monster and Player Framework

This module creates the framework for different types of monster enemies and
the framework for the player character (including controls).
"""

__version__ = "0.2"
__author__ = "Reuben Wiles Maguire"

from pgzero.builtins import Actor, keyboard, keys
from constants import *
from numpy import hypot
from time import time
from random import randint


def normalise(dx, dy):
    """Normalises a vector.
    
    Parameters
    ----------
    dx : float          - x component of vector
    dy : float          - y component of vector
    
    Return
    ------
    (float, float)      - normalised vector
    """

    hyp = hypot(dx, dy)
    if hyp != 0:
        return [dx, dy] / hyp
    else:
        return (0, 0)


class Base_Actor(Actor):
    """A class that describes the basic functions of the games creatures.

    Attributes
    ----------
    img_base : str      - the name of the image
    img_direction : str - the current direction of the image
    img_frame : str     - the current frame of animation
    img_dir : str       - the sub directory of the image (optional)
    img_hurt_frame : int    - how long the image has been in the hurt state
    img_frame_counter : int - how long the image has been in the current frame
    image : str         - combination of above attributes
    speed : int         - speed of creature
    health : int        - health of creature
    x_pos : float       - x coordinate of creature
    y_pos : float       - y coordinate of creature
    dx : float          - x component of creature movement
    dy : float          - y component of creature movement
    alive : bool        - if the mob is alive
    damage_death : bool - if the mob was killed by damage and not a collision
                          with the player


    "image" Explained
    -----------------
            img_dir      img_frame   
               |             |
    image = example\\example_2l.png
                        |     |
                   img_base  img_direction

    Methods
    -------
    hurt(damage)        - Reduces the creatures health by "damage" and sets the 
                          number of hurt frames to "HURT_DURATION". If health is
                          reduced to 0, sets "alive" to False.
    collision(player) : bool    - Placeholder to be overwritten by children.
    move(player)        - Moves the creature by (dx, dy)*speed incrementally and
                          runs sets "alive" to False if "collision" returns 
                          True.
    update(player)      - Runs every game update. Works out the next animation 
                          frame and updates it. Runs "move".
    draw(offset_x, offset_y)    - Calculates where to draw creature. Then, calls
                          parent "draw".
    """

    def __init__(self, img, x, y, speed, health, img_dir=""):
        """Constructs the Base_Actor class.

        Parameters
        ----------
        img : str           - image name (without frame number or direction)
        x : int             - starting x coordinate of creature
        y : int             - starting y coordinate of creature
        speed : int         - speed of creature
        health : int        - health of creature
        img_dir : str       - sub directory of image (optional)
        """

        self.img_base = img
        self.img_direction = "r"
        self.img_frame = 1
        self.img_dir = img_dir
        if img_dir != "":
            self.img_dir += "\\"
        cur_img = f"{self.img_dir}{self.img_base}"\
                  f"_{self.img_direction}{self.img_frame}"
                  
        super().__init__(cur_img, (x, y))
        self.speed = speed
        self.health = health
        self.x_pos = x
        self.y_pos = y
        self.dx = 0
        self.dy = 0
        self.img_hurt_frame = 0
        self.img_frame_counter = 0
        self.alive = True
        self.damage_death = False
    
    def hurt(self, damage):
        """Reduces the creatures health by "damage" and sets "img_hurt_frame" 
        to "HURT_DURATION". If health is reduced to 0 or less, set "alive" to 
        False.

        Parameters
        ----------
        damage : int        - amount to reduce "health" by
        """

        self.health -= damage
        self.img_hurt_frame = HURT_DURATION
        if self.health <= 0:
            self.damage_death = True
            self.alive = False

    def collision(self, player):
        """Placeholder to be overwritten by children. Returns False."""
        return False

    def move(self, player):
        """Moves the creature by (dx, dy)*speed incrementally. Each increment 
        run "collision" and if True is returned, sets "alive" to False.

        Parameters
        ----------
        player : obj        - the player character object
        """

        for i in range(self.speed):
            if self.collision(player):
                self.alive = False
            self.x_pos += self.dx
            self.y_pos += self.dy

    def update(self, player):
        """Runs every game update. Works out the next animation frame based on 
        the creature direction, current frame, and hurt status. Then runs move.

        Parameters
        ----------
        player : obj        - the player character object
        """
        self.img_frame_counter += 1
        if self.img_frame_counter > FRAME_TIME:
            self.img_frame_counter = 0
            self.img_frame += 1
        if self.img_frame > MAX_ANIMATION_FRAMES:
            self.img_frame = 1

        if self.dx < 0:
            self.img_direction = "l"
        elif self.dx > 0:
            self.img_direction = "r"

        self.image = f"{self.img_dir}{self.img_base}"\
                     f"_{self.img_direction}{self.img_frame}"

        
        if self.img_hurt_frame > 0:
            self.image += "_hurt"
            self.img_hurt_frame -= 1
        
        self.move(player)

    def draw(self, offset_x, offset_y):
        """Calculates where to draw creature. Then, calls parent "draw".
        
        Parameters
        ----------
        offset_x : float    - difference between real and virtual x position
        offset_y : float    - difference between real and virtual y position
        """

        self.pos = (self.x_pos - offset_x, self.y_pos - offset_y)
        super().draw()
        

class Player(Base_Actor):
    """A class that describes the player character.

    Child of Base_Actor

    Attributes
    ----------
    max_health : int    - max health of the player

    Methods
    -------
    move(player)        - Moves the player by (dx, dy)*speed incrementally and
                          checks that the player is not moving out of the levels
                          bounds.
    movement_direction()
    update()
    """
    __doc__ += Base_Actor.__doc__

    def __init__(self, img, x, y, speed, health, img_dir=""):
        """Constructs the Player class.

        Parameters
        ----------
        img : str           - image name (without frame number or direction)
        x : int             - starting x coordinate of creature
        y : int             - starting y coordinate of creature
        speed : int         - speed of creature
        health : int        - health of creature
        img_dir : str       - sub directory of image (optional)
        """

        super().__init__(img, x, y, speed, health, img_dir)
        self.max_health = health
    
    def move(self, player):
        """Moves the player by (dx, dy)*speed incrementally. Each increment 
        check the player is not about to move out of bounds and if they are
        stop them.

        Parameters
        ----------
        player : obj        - the player character object
        """

        for i in range(self.speed):
            self.x_pos += self.dx
            self.x_pos = max(0 + PLAYER_W, min(self.x_pos, LEVEL_W - PLAYER_W))
            self.y_pos += self.dy
            self.y_pos = max(0 + PLAYER_H, min(self.y_pos, LEVEL_H - PLAYER_H))
            
    def movement_direction(self):
        """Calculates the players movement direction based on keyboard inputs
        and normalises dx and dy.
        """

        self.dx = 0
        self.dy = 0

        if keyboard.right or keyboard.d:
            self.dx += 1
        if keyboard.left or keyboard.a:
            self.dx -= 1
        if keyboard.up or keyboard.w:
            self.dy -= 1
        if keyboard.down or keyboard.s:
            self.dy += 1
        
        self.dx, self.dy = normalise(self.dx, self.dy)
    
    def update(self):
        """Runs every game update. Runs "movement_direction" and parents 
        "update".
        """
        
        self.movement_direction()
        super().update(self)

        if self.dx == 0 and self.dy == 0:
            self.image = f"{self.img_dir}{self.img_base}_idle"

        


class Monster(Base_Actor):
    """A class that describes basic monsters.

    Child of Base_Actor

    Attributes
    ----------
    damage : int        - damage dealt by monster
    xp_value : int      - the xp value of the monster

    Methods
    -------
    calculate_direction(player) : (float, float)    - Finds the direction of the
                          player character from the mosters current position.
    collision(player) : bool    - Detects collisions between the monster and 
                          the player.
    update(player)      - Runs every game update. Runs "calculate_direction" and
                          parents "update".
    
    Parent
    ------
    """
    __doc__ += Base_Actor.__doc__

    def __init__(self, img, screen_coords, speed, health, damage, xp_value, 
                 img_dir=""):
        """Constructs the Monster class.

        Parameters
        ----------
        img : str           - image name (without frame number or direction)
        screen_coords : (int, int, int, int) - coordinates of the screen
        speed : int         - speed of monster
        health : int        - health of monster
        damage : int        - damage dealt by monster
        xp_value : int      - the xp value of the monster
        img_dir : str       - sub directory of image (optional)
        """
        self.xp_value = xp_value
        self.damage = damage
        spawn_coords = self.calculate_spawn_coords(screen_coords)
        super().__init__(img, spawn_coords[0], spawn_coords[1], speed, health, 
                         img_dir)

    def calculate_spawn_coords(self, screen_coords):

        LEFT = 0
        TOP = 1
        RIGHT = 2
        BOTTOM = 3

        side = randint(0,3)    
        
        if (side == LEFT):
            posx = max(screen_coords[LEFT] - SPAWN_DISTANCE, 0)
            posy = randint(screen_coords[TOP],screen_coords[BOTTOM])      
        elif (side == TOP): 
            posx = randint(screen_coords[LEFT],screen_coords[RIGHT])
            posy = max(screen_coords[TOP] - SPAWN_DISTANCE, 0)
        elif (side == RIGHT): 
            posx = min(screen_coords[RIGHT] + SPAWN_DISTANCE, LEVEL_W)
            posy = randint(screen_coords[TOP],screen_coords[BOTTOM])
        elif (side == BOTTOM):
            posx = randint(screen_coords[LEFT],screen_coords[RIGHT])
            posy = min(screen_coords[BOTTOM] + SPAWN_DISTANCE, LEVEL_H)
        
        return (posx, posy)
    
    def calculate_direction(self, player):
        """Runs "normalise" on the difference between the players (x, y) and the
        monsters (x, y) to calculate the direction of the player character.

        Parameter
        ---------
        player : obj        - the player character object

        Return
        ------
        (float, float)      - normalised vector of the line between the player
                              and the monster.
        """

        return normalise(player.x_pos - self.x_pos, player.y_pos - self.y_pos)
    
    def collision(self, player):
        """Detects collisions between the monster and the player. Returns
        True if a collision occurs.
        
        Parameters
        ----------
        player : obj        - the player character object
        
        Return
        ------
        bool                - if a collison has occured or not
        """

        if self.colliderect(player):
            player.hurt(self.damage)
            return True
        return False

    def update(self, player):
        """Runs every game update. Runs "calculate_direction" to set dx and dy.
        Then runs parents "update".

        Parameters
        ----------
        player : obj        - the player character object
        """

        self.dx, self.dy = self.calculate_direction(player)
        super().update(player)


class Charger(Monster):
    """A class describing monsters that charge in a straight line.
    
    Child of Monster

    Attributes
    ----------
    cooldown_start : float  - the time at which the charger last dealt damage

    Methods
    -------
    collision(player) : bool    - Dectects collisions between the charger and 
                          the player character and runs "hurt" if its attack is
                          not on cooldown.
    update(player)      - Runs every game update. Sets "alive" to False if the 
                          charger runs off the edge of the level. Then runs  
                          parents "update".
    
    Parent
    ------
    """
    __doc__ += Monster.__doc__

    def __init__(self, img, screen_coords, speed, health, damage, player, 
                 img_dir=""):
        """Constructs the Charger class.
        
        Parameters
        ----------
        img : str           - image name (without frame number or direction)
        screen_coords : (int, int, int, int) - coordinates of the screen
        speed : int         - speed of monster
        health : int        - health of monster
        damage : int        - damage dealt by monster
        player : obj        - the player character object
        img_dir : str       - sub directory of image (optional)
        """

        self.cooldown_start = -1.0
        super().__init__(img, screen_coords, speed, health, damage, img_dir)
        self.dx, self.dy = self.calculate_direction(player)
    
    def collision(self, player):
        """Dectects collisions between the charger and the player character and 
        runs "hurt" if its attack is not on cooldown. When a collision occurs
        the time is recorded and another collision can't occur until 
        "HURT_COOLDOWN" is exceded.

        Parameters
        ----------
        player : obj        - the player character object

        Return
        ------
        bool                - always returns False
        """

        if self.colliderect(player) and self.cooldown_start == -1.0:
            player.hurt(self.damage)
            self.cooldown_start = time()
        elif time() - self.cooldown_start >= HURT_COOLDOWN:
            self.cooldown_start = -1.0
        return False
    
    def update(self, player):
        """Runs every game update. Sets "alive" to False if the charger runs off
        the edge of the level. Then runs parents "update".

        Parameters
        ----------
        player : obj        - the player character object
        """
        
        if (self.x_pos < -100 or self.x_pos > LEVEL_W + 100 or 
            self.y_pos < -100 or self.y_pos > LEVEL_H + 100):
            self.alive = False
        super(Monster, self).update(player)

