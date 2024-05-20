"""Level Up

This module defines the Level_Up class. This class handles the functionality and
UI of the level up screen.
"""
__version__ = "0.4"
__author__ = "Reuben Wiles Maguire"

from pgzero.builtins import keyboard, keys
from constants import LEVEL_UP_TEXT_X, LEVEL_UP_TEXT_Y,\
LEVEL_UP_TEXT_Y_SEP, LEVEL_UP_TEXT_WIDTH, LEVEL_UP_SCREEN_DELAY


class Level_Up():
    """A class that describes the functionality of the level up screen.

    Attributes
    ----------
    choices : [obj, ...]        - a list of the options to pick from
    all_max_level : bool        - if all weapons are at their max level
    current_selection : int     - currently selected option in the level up menu
    chosen : bool               - if the player has chosen an option from the 
                                  menu
    option_chosen : obj         - the option the player chose from the menu
    down_pressed : bool         - if the player pressed down in the last frame
    up_pressed : bool           - if the player pressed up in the last frame
    show_screen_delay : int     - counter that tracks how many times "draw" has
                                  been called before "draw" is allowed to run

    Methods
    -------
    is_chosen() : bool          - Returns "chosen".
    get_choice() : obj          - Returns "option_chosen".
    update()                    - Runs every game update. Detects if the player 
                                  presses up or down and changes 
                                  "current_selection" accordingly. Detects if 
                                  the player presses space and selects the 
                                  current option as the chosen option and sets 
                                  "chosen" to True. If there are no options to 
                                  choose from, sets "chosen" to True 
                                  automatically.
    draw()                      - Runs every game update. Draws the current 
                                  state of the level up screen.
    """

    def __init__(self, current_weapons):
        """Constructs the Level_Up class.
        
        Parameters
        ----------
        current_weapons : [obj, ...]    - a list of the players weapons
        """

        self.choices = current_weapons
                    
        self.all_max_level = True
        for weapon in self.choices:
            if not weapon.max_level:
                self.all_max_level = False

        self.current_selection = 0

        self.chosen = False
        self.option_chosen = None

        self.down_pressed = False
        self.up_pressed = False

        self.show_screen_delay = 0

    def is_chosen(self):
        """Returns "chosen"."""

        return self.chosen
    
    def get_choice(self):
        """Returns "option_chosen"."""

        return self.option_chosen
    
    def update(self):
        """Runs every game update. Detects if the player presses up or down and
        changes "current_selection" accordingly. Detects if the player presses
        space and selects the current option as the chosen option and sets 
        "chosen" to True.
        If there are no options to choose from, sets "chosen" to True 
        automatically.
        """

        if not self.chosen and not self.all_max_level:
            if (keyboard.up or keyboard.w) and not self.up_pressed:
                self.up_pressed = True
                if self.current_selection == 0:
                    self.current_selection = len(self.choices) - 1
                else:
                    self.current_selection -= 1
            elif not (keyboard.up or keyboard.w):
                self.up_pressed = False

            if (keyboard.down or keyboard.s) and not self.down_pressed:
                self.down_pressed = True
                if self.current_selection == len(self.choices) - 1:
                    self.current_selection = 0
                else:
                    self.current_selection += 1
            elif not (keyboard.down or keyboard.s):
                self.down_pressed = False
        
            if keyboard.space:
                if not self.choices[self.current_selection].max_level:
                    self.chosen = True
                    self.option_chosen = self.choices[self.current_selection]
        elif not self.chosen and self.all_max_level:
            self.chosen = True

    def draw(self, screen):
        """Runs every game update. Draws the current state of the level up 
        screen.
        """

        if not self.chosen and self.show_screen_delay > LEVEL_UP_SCREEN_DELAY:
            screen.blit("level_up", (0, 0))

            for i in range(len(self.choices)):
                screen.draw.text(self.choices[i].description, 
                                 (LEVEL_UP_TEXT_X, 
                                  LEVEL_UP_TEXT_Y + LEVEL_UP_TEXT_Y_SEP * i), 
                                  fontname="vcr_osd_mono_1.001", fontsize=20,
                                  color="black", width=LEVEL_UP_TEXT_WIDTH)

            screen.blit("level_up_select_"+str(self.current_selection), (0, 0))
        else:
            self.show_screen_delay += 1