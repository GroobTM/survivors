from pgzero.builtins import Actor, keyboard, keys
from constants import MAX_ANIMATION_FRAMES, LEVEL_H, LEVEL_W
from globals import player_pos
from numpy import hypot
from time import time

HURT_DURATION = 2
HURT_COOLDOWN = 10

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

    return [dx, dy] / hypot(dx, dy)

class Base_Actor(Actor):
    """A class that describes the basic functions of the games creatures.

    Attributes
    ----------
    img_base : str      - the name of the image
    img_direction : str - the current direction of the image
    img_frame : str     - the current frame of animation
    img_dir : str       - the sub directory of the image (optional)
    img_hurt_frame : int    - how long the image has been in the hurt state
    image : str         - combination of above attributes
    speed : int         - speed of creature
    health : int        - health of creature
    x : int             - x coordinate of creature
    y : int             - y coordinate of creature
    dx : float          - x component of creature movement
    dy : float          - y component of creature movement

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
                          number of hurt frames to "HURT_DURATION".
    collision(player)   - Placeholder to be overwritten by children.
    remove()            - Deletes the creature.
    move(player)        - Moves the creature by (dx, dy)*speed incrementally and
                          runs "remove" if "collision" returns True.
    update(player)      - Runs every game update. Works out the next animation 
                          frame and updates it. Runs "move".
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
        cur_img = f"{self.img_dir}{self.img_base}_{self.img_direction}\
        {self.img_frame}"
        super().__init__(cur_img, (x, y))
        self.speed = speed
        self.health = health
        self.dx = 0
        self.dy = 0
        self.img_hurt_frame = 0
        
    def hurt(self, damage):
        """Reduces the creatures health by "damage" and sets "img_hurt_frame" 
        to "HURT_DURATION".

        Parameters
        ----------
        damage : int        - amount to reduce "health" by
        """

        self.health -= damage
        self.img_hurt_frame = HURT_DURATION

    def collision(self, player):
        """Placeholder to be overwritten by children. Returns False."""
        return False

    def remove(self):
        """Deletes the creature."""

        del self

    def move(self, player):
        """Moves the creature by (dx, dy)*speed incrementally. Each increment 
        run "collision" and if True is returned, run "remove".

        Parameters
        ----------
        player : obj        - the player character object
        """

        for i in self.speed():
            if self.collision(player):
                self.remove()
            self.x += self.dx
            self.y += self.dy

    def update(self, player):
        """Runs every game update. Works out the next animation frame based on 
        the creature direction, current frame, and hurt status. Then runs move.

        Parameters
        ----------
        player : obj        - the player character object
        """

        self.img_frame += 1
        if self.img_frame > MAX_ANIMATION_FRAMES:
            self.img_frame = 1

        if self.dx < 0:
            self.img_direction = "l"
        elif self.dx > 0:
            self.img_direction = "r"

        self.image = f"{self.img_dir}{self.img_base}_{self.img_direction}\
            {self.img_frame}"
        
        if self.img_hurt_frame > 0:
            self.image += "_hurt"
            self.img_hurt_frame -= 1

        self.move(player)

class Monster(Base_Actor):
    """A class that describes basic monsters.

    Child of Base_Actor

    Attributes
    ----------
    damage : int        - damage dealt by monster

    Methods
    -------
    calculate_direction(player) - Finds the direction of the player character 
                          from the mosters current position.
    collision(player)   - Detects collisions between the monster and the player.
    update(player)      - Runs every game update. Runs "calculate_direction" and
                          parents "update".
    
    Parent
    ------
    """
    __doc__ += super.__doc__

    def __init__(self, img, x, y, speed, health, damage, img_dir=""):
        """Constructs the Monster class.

        Parameters
        ----------
        img : str           - image name (without frame number or direction)
        x : int             - starting x coordinate of monster
        y : int             - starting y coordinate of monster
        speed : int         - speed of monster
        health : int        - health of monster
        damage : int        - damage dealt by monster
        img_dir : str       - sub directory of image (optional)
        """

        self.damage = damage
        super().__init__(img, x, y, speed, health, img_dir)

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

        return normalise(player.x - self.x, player.y - self.y)
    
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
    collision(player)   - Dectects collisions between the charger and the player
                          character and runs "hurt" if its attack is not on 
                          cooldown.
    update(player)      - Runs every game update. Runs "remove" if the charger
                          runs off the edge of the level. Then runs parents 
                          "update".
    
    Parent
    ------
    """
    __doc__ += super.__doc__

    def __init__(self, img, x, y, speed, health, damage, player, img_dir=""):
        """Constructs the Charger class.
        
        Parameters
        ----------
        img : str           - image name (without frame number or direction)
        x : int             - starting x coordinate of monster
        y : int             - starting y coordinate of monster
        speed : int         - speed of monster
        health : int        - health of monster
        damage : int        - damage dealt by monster
        player : obj        - the player character object
        img_dir : str       - sub directory of image (optional)
        """

        self.cooldown_start = -1.0
        super().__init__(img, x, y, speed, health, damage, img_dir)
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
        """Runs every game update. Runs "remove" if the charger runs off the 
        edge of the level. Then runs parents "update".

        Parameters
        ----------
        player : obj        - the player character object
        """
        
        if (self.x < -100 or self.x > LEVEL_W + 100 or 
            self.y < -100 or self.y > LEVEL_H + 100):
            self.remove()
        super(Monster, self).update(player)