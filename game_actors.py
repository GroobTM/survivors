from pgzero.builtins import Actor, keyboard, keys
from constants import MAX_ANIMATION_FRAMES
from globals import player_pos
from numpy import hypot

HURT_EXT = "_hurt"
HURT_DURATION = 2

def normalise(dx, dy):
    return [dx, dy] / hypot(dx, dy)

class Base_Actor(Actor):
    def __init__(self, img, x, y, speed, health, dir=""):
        self.img_base = img
        self.img_direction = "r"
        self.img_frame = 1
        self.dir = dir
        if dir != "":
            self.dir += "\\"
        cur_img = f"{self.dir}{self.img_base}_{self.img_direction}\
        {self.img_frame}"
        super().__init__(cur_img, (x, y))
        self.speed = speed
        self.health = health
        self.dx = 0
        self.dy = 0
        self.img_hurt_frame = 0
        
    def hurt(self, damage):
        self.health -= damage
        self.img_hurt_frame = HURT_DURATION

    def collision(self, player):
        return False

    def remove(self):
        """Deletes the actor."""

        del self

    def move(self, player):
        for i in self.speed():
            if self.collision(player):
                self.remove()
            self.x += self.dx
            self.y += self.dy

    def update(self, player):

        # Figures out which frame to switch to
        self.img_frame += 1
        if self.img_frame > MAX_ANIMATION_FRAMES:
            self.img_frame = 1

        if self.dx < 0:
            self.img_direction = "l"
        elif self.dx > 0:
            self.img_direction = "r"

        self.image = f"{self.dir}{self.img_base}_{self.img_direction}\
            {self.img_frame}"
        
        if self.img_hurt_frame > 0:
            self.image += HURT_EXT
            self.img_hurt_frame -= 1

        self.move(player)

class Monster(Base_Actor):
    def __init__(self, img, x, y, speed, health, damage, dir=""):
        self.damage = damage
        super().__init__(img, x, y, speed, health, dir)

    def calculate_direction(self):
        return normalise(player_pos[0] - self.x, player_pos[1] - self.y)
    
    def collision(self, player):
        if self.colliderect(player):
            player.hurt(self.damage)
            return True
        return False

    def update(self, player):
        self.dx, self.dy = self.calculate_direction()
        super().update(player)