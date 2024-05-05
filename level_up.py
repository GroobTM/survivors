from pgzero.builtins import keyboard, keys
from random import sample
from constants import LEVEL_UP_CHOICES_COUNT
from weapons import Thrown_Dagger, Arrow, Magic_Missile


WEAPON_LIST = [Thrown_Dagger(), Arrow(), Magic_Missile()]

class Level_Up():
    def __init__(self, current_weapons):
        self.current_weapons = current_weapons
        self.possible_choices = WEAPON_LIST
        self.shown_choices = []
        self.find_choices()

        self.current_selection = 0

        self.chosen = False
        self.option_chosen = None

        self.down_pressed = False
        self.up_pressed = False

    def find_choices(self):
        for current_weapon in self.current_weapons:
            for new_weapon in WEAPON_LIST:
                if type(current_weapon) == type(new_weapon):
                    print(new_weapon)
                    self.possible_choices.remove(new_weapon)

            if not current_weapon.max_level:
                current_weapon.level_up_weapon()
                self.possible_choices.append(current_weapon)

        choices_count = len(self.possible_choices)
        if choices_count == 0:
            self.chosen = True
        elif choices_count < 3:
            self.shown_choices = self.possible_choices
        else:
            self.shown_choices = sample(self.possible_choices, 
                                        LEVEL_UP_CHOICES_COUNT)

    def is_chosen(self):
        return self.chosen
    
    def get_choice(self):
        return self.option_chosen
    
    def update(self):
        if not self.chosen:
            if (keyboard.up or keyboard.w) and not self.up_pressed:
                self.up_pressed = True
                if self.current_selection == 0:
                    self.current_selection == LEVEL_UP_CHOICES_COUNT - 1
                else:
                    self.current_selection -= 1
            elif not (keyboard.up or keyboard.w):
                self.up_pressed = False

            if (keyboard.down or keyboard.s) and not self.down_pressed:
                self.down_pressed = True
                if self.current_selection == LEVEL_UP_CHOICES_COUNT - 1:
                    self.current_selection == 0
                else:
                    self.current_selection += 1
            elif not (keyboard.down or keyboard.s):
                self.down_pressed = False

            if keyboard.space:
                self.chosen = True
                self.option_chosen = self.shown_choices[self.current_selection]

    def draw(self):
        print(self.shown_choices[self.current_selection].name, 
              self.shown_choices[self.current_selection].level)