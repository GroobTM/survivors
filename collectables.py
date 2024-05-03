"""Collectables Framework

This module creates the framework for the different types of collectables that
can spawn when killing a monster.
"""

__version__ = "0.1"
__author__ = "Reuben Wiles Maguire"

from pgzero.builtins import Actor
from constants import HEAL_VALUE


class Base_Collectable(Actor):#
    """A class that describes the basic functions of collectables.

    Attributes
    ----------
    x_pos : float           - x coordinate of the collectable
    y_pos : float           - y coordinate of the collectable
    visible : bool          - if the collectable can be seen and interacted with
    exists : bool           - if the collectable exists
    active : bool           - if the effect of the collectable is active

    Methods
    -------
    collide_player(player)  - Makes the collectable invisible and activates it
                              if the player collides with it.
    active_effect(game)     - Sets the collectable to no longer exist.
    update(game)            - Run every game update. Runs "collide_player" and
                              if the collectable is active, runs 
                              "active_effect".
    draw(offset_x, offset_y)    - Runs every game update. If the collectable is
                              visible, calculates where to draw the collectable
                              and calls parent "draw".
    """

    def __init__(self, img, monster):
        """Constructs the Base_Collectable class.
        
        Parameters
        ----------
        img : str               - path of an image file in ./images used for 
                                  collectable sprite
        monster : obj           - the monster object of the monster that spawns
                                  the collectable when it dies
        """

        super().__init__(img, (monster.x_pos, monster.y_pos))
        self.x_pos = monster.x_pos
        self.y_pos = monster.y_pos

        self.visible = True
        self.exists = True
        self.active = False

    def collide_player(self, player):
        """Detects collisions between the player and the collectable. Makes the 
        collectable invisible and activates it if the player collides with it.

        Parameters
        ----------
        player : obj            - the player object
        """

        if self.visible and self.colliderect(player):
            self.visible = False
            self.active = True

    def active_effect(self, game):
        """Sets the collectable to no longer exist.

        Parameters
        ----------
        game : obj              - the game object
        """

        self.exists = False

    def update(self, game):
        """Run every game update. Runs "collide_player" and if the collectable 
        is active, runs "active_effect".
        
        Parameters
        ----------
        game : obj              - the game object
        """

        self.collide_player(game.player)
        
        if self.active:
            self.active_effect(game)

    def draw(self, offset_x, offset_y):
        """Runs every game update. If the collectable is visible, calculates 
        where to draw the collectable and calls parent "draw".
        
        Parameters
        ----------
        offset_x : float    - difference between real and virtual x position
        offset_y : float    - difference between real and virtual y position
        """

        if self.visible:
            self.pos = (self.x_pos - offset_x, self.y_pos - offset_y)
            super().draw()

class XP(Base_Collectable):
    """A class that describes XP.

    Child of Base_Collectable

    Attributes
    ----------
    value : int         - the amount of XP given by the collectable

    Methods
    -------
    active_effect(game) - Adds the collectables value to the xp counter and 
                          runs parent "active_effect".

    Parent
    ------
    """
    __doc__ += Base_Collectable.__doc__

    def __init__(self, monster):
        """Constructs the XP class.
        
        Parameters
        ----------
        monster : obj       - the monster object of the monster that spawns
                              the collectable when it dies
        """

        self.value = monster.xp_value
        img = "collectables\\xp"

        # Select the correct XP level image based on the value.
        if self.value < 10:
            img += "1"
        elif self.value < 50:
            img += "2"
        else:
            img += "3"
        super().__init__(img, monster)
        
    def active_effect(self, game):
        """Adds the collectables value to the xp counter and runs parent 
        "active_effect".

        Parameters
        ----------
        game : obj          - the game object
        """

        game.xp += self.value
        super().active_effect(game)

class Cake(Base_Collectable):
    """A class that describes a cake healing item.

    Child of Base_Collectable

    Attributes
    ----------
    heal_value : int        - the amount of health restored by the collectable

    Methods
    -------
    active_effect(game)     - Increases the players current health by the cakes
                              healing value. Reduces the players health to its
                              maximum if its value exceeds it. Runs parent
                              "active_effect".
    
    Parent
    ------
    """
    __doc__ += Base_Collectable.__doc__

    def __init__(self, monster):
        """Constructs the Cake class.
        
        Parameters
        ----------
        monster : obj       - the monster object of the monster that spawns
                              the collectable when it dies
        """

        super().__init__("collectables\\cake", monster)
        self.heal_value = HEAL_VALUE

    def active_effect(self, game):
        """Increases the players current health by the cakes healing value. 
        Reduces the players health to its maximum if its value exceeds it. 
        Runs parent "active_effect".

        Parameters
        ----------
        game : obj          - the game object
        """

        game.player.health += self.heal_value
        if game.player.health > game.player.max_health:
            game.player.health = game.player.max_health
        super().active_effect(game)