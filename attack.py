from pgzero.builtins import Actor
from time import time
from random import randint
from numpy import hypot
from constants import WIDTH, ATTACK_IMMUNE
from game_actors import normalise

class Attack(Actor):
    """A class that describes the properties of a basic attack.
    
    The attack described travels in a straight line in the direction of the
    player's movement when the attack was created (randomly if player is not
    moving).

    Attributes
    ----------
    img : str           - name of a png file in ./images used for sprite
    x_pos : int         - x coordinate of the attack
    y_pos : int         - y coordinate of the attack
    dx : float          - x vector of movement
    dy : float          - y vector of movement
    speed : int         - speed of movement
    damage : int        - damage of the attack
    duration : float    - how long the attack lasts before it is removed
    pierce : int        - how many enemies the attack can pierce before it is
                          removed
    spawn_time : float  - when the attack was created
    exists : bool       - marks the object for removal
    immune_counter : int    - how long the attack should be prevented from
                          dealing damage to the last monster hit
    last_hit : obj      - the last monster hit by the attack

    Methods
    -------
    collision(mob_list) - Detects collisions between the attack and mobs.
    check_duration()    - Checks how long the attack has existed and marks it
                          for removal if necessary.
    move(mob_list)      - Moves the attack incrementally and runs "collision".
    update(mob_list)    - Runs every game update. Runs "move" and 
                          "check_duration".
    draw(offset_x, offset_y)    - Adjusts the attacks position based on the
                          position of the screen and runs parent "draw".
    """

    def __init__(self, img, player, speed, damage, duration, pierce=-1):
        """Constructs the Attack class.

        Parameters
        ----------
        img : str           - name of a png file in ./images used for sprite
        player : obj        - the player character object
        speed : int         - speed of movement
        damage : int        - damage of the attack
        duration : float    - how long the attack lasts before it is removed
        pierce : int        - how many enemies the attack can pierce before it
                              is removed (-1 means infinite)
        """

        super().__init__(img, (player.x_pos, player.y_pos))
        self.x_pos = player.x_pos
        self.y_pos = player.y_pos
        self.dx = player.dx
        self.dy = player.dy
        # Prevents stationary attacks
        while self.dx == 0 and self.dy == 0:
            self.dx, self.dy = normalise(randint(-1, 1), randint(-1, 1))
        self.speed = speed
        self.damage = damage
        self.duration = duration
        self.pierce = pierce

        self.spawn_time = time()
        self.exists = True
        self.immune_counter = 0
        self.last_hit = None
        
    def collision(self, mob_list):
        """Detects collisions between the attack and mobs. When a collision is
        detected, cause damage to that mob and reduce the pierce counter. If
        pierce reaches 0, mark the attack for removal. Prevents collisions if
        the weapon has damaged the same monster too recently.

        Parameters
        ----------
        mob_list : [obj, ...]   - list of all currently alive mobs
        """

        
        collision_index = self.collidelist(mob_list)
        if collision_index != -1:
            if (self.last_hit != mob_list[collision_index] or 
                self.immune_counter == 0):
                mob_list[collision_index].hurt(self.damage)
                self.last_hit = mob_list[collision_index]
                self.immune_counter = ATTACK_IMMUNE
                self.pierce -= 1
                if self.pierce == 0:
                    self.exists = False

    def check_duration(self):
        """Checks how long the attack has existed and marks it for removal if
        the time it has existed for excedes the attacks duration.
        """

        if time() - self.spawn_time >= self.duration:
            self.exists = False

    def move(self, mob_list):
        """Moves the attack incrementally by (dx, dy)*speed and runs "collision"
        at each increment.

        Parameters
        ----------
        mob_list : [obj, ...]   - list of all currently alive mobs
        """

        for i in range(self.speed):
            self.x_pos += self.dx
            self.y_pos += self.dy
            self.collision(mob_list)

    def update(self, mob_list):
        """Runs every game update. Runs "move" and "check_duration".

        Parameters
        ----------
        mob_list : [obj, ...]   - list of all currently alive mobs 
        """
        if self.immune_counter > 0:
            self.immune_counter -= 1
        self.move(mob_list)
        self.check_duration()

    def draw(self, offset_x, offset_y):
        """Adjusts the attacks position based on the position of the screen and 
        runs parent "draw".

        Parameters
        ----------
        offset_x : int      - offset for the screens real and virtual x position
        offset_y : int      - offset for the screens real and virtual y position
        """

        self.pos = (self.x_pos - offset_x, self.y_pos - offset_y)
        super().draw()


class Aimed_Attack(Attack):
    """A class that describes attacks that are aimed at the closest monster.
    These attacks can be homing causing them to seek out their target.

    Child of Attack

    Attributes
    ----------
    homing : bool       - whether the attack is homing or not
    target : obj        - the attacks current target

    Methods
    -------
    find_closest(mob_list)  - Finds the mob closest to the object and sets it as
                          the target.
    calc_direction(mob_list)    - Calculates the direction of the target mob.
    update(mob_list)    - Runs every game update. If the attack is homing runs
                          "calc_direction". Runs parents update.
    
    Parent
    ------
    """
    __doc__ += Attack.__doc__

    def __init__(self, img, player, mob_list, speed, damage, duration, 
                 pierce=-1, homing=False):
        """Constructs the Aimed_Attack class.

        Parameters
        ----------
        img : str           - name of a png file in ./images used for sprite
        player : obj        - the player character object
        mob_list : [obj, ...]   - list of all currently alive mobs
        speed : int         - speed of movement
        damage : int        - damage of the attack
        duration : float    - how long the attack lasts before it is removed
        pierce : int        - how many enemies the attack can pierce before it
                              is removed (-1 means infinite)
        homing : bool       - if the attack is aimed or not
        """

        super().__init__(img, player, speed, damage, duration, pierce)
        self.homing = homing
        
        self.target = None
        self.calc_direction(mob_list)

    def find_closest(self, mob_list):
        """Finds the mob closest to the object and sets it as the target.

        Parameters
        ----------
        mob_list : [obj, ...]   - list of all currently alive mobs
        """

        distance = WIDTH
        for mob in mob_list:
            new_distance = hypot(mob.x_pos - self.x_pos, mob.y_pos - self.y_pos)
            if new_distance < distance:
                distance = new_distance
                self.target = mob

    def calc_direction(self, mob_list):
        """Calculates the direction of the target mob and sets dx and dy 
        accordingly. If the target has not been set, runs "find_closest".
        If there is no available target, set dx and dy randomly.

        Parameters
        ----------
        mob_list : [obj, ...]   - list of all currently alive mobs
        """

        if self.target not in mob_list:
            self.find_closest(mob_list)
        
        if self.target == None:
            while self.dx == 0 and self.dy == 0:
                self.dx, self.dy = normalise(randint(-1, 1), randint(-1, 1))
        else:
            x_difference = self.target.x_pos - self.x_pos
            y_difference = self.target.y_pos - self.y_pos

            self.dx, self.dy = normalise(x_difference, y_difference)

    def update(self, mob_list):
        """Runs every game update. If the attack is homing runs 
        "calc_direction". Then, runs parents update.

        Parameters
        ----------
        mob_list : [obj, ...]   - list of all currently alive mobs
        """
        if self.homing:
            self.calc_direction(mob_list)

        super().update(mob_list)