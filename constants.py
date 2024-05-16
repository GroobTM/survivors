# Size of the game window
WIDTH = 1024
HEIGHT = 768
HALF_WINDOW_W = WIDTH / 2
HALF_WINDOW_H = HEIGHT / 2

# Size of level and player
LEVEL_W = 2250
LEVEL_H = 1500
HALF_LEVEL_W = LEVEL_W // 2
HALF_LEVEL_H = LEVEL_H // 2

PLAYER_W = 16
PLAYER_H = 32

# Animation
MAX_ANIMATION_FRAMES = 4
FRAME_TIME = 20
HURT_DURATION = 2
HURT_COOLDOWN = 10

# Spawning
SPAWN_RATE = (20, 20, 15, 15, 10, 10, 5, 5)
SPAWN_DISTANCE = 50

# Attacks
ATTACK_DELAY = 0.2
ATTACK_IMMUNE = 30

# GUI
BAR_HEIGHT = 40
BAR_BORDER = 5
NUMBER_WIDTH = 29
NUMBER_HEIGHT = 40
NUMBER_GAP = 6
HALF_NUMBER_GAP = NUMBER_GAP / 2
TIMER_SEPARATION = NUMBER_GAP + NUMBER_WIDTH

# Balance
CONDENSE_THRESHOLD = 50
CONDENSE_AMOUNT = 10
CONDENSE_DISTANCE = (20, 40, 60)
HEAL_VALUE = 20
HEAL_SPAWN_CHANCE = 1
LEVEL_CAP_MULTIPLIER = 1.1
LEVEL_CAP_BASE = 20
LEVEL_UP_CHOICES_COUNT = 3

# Player
PLAYER_SPRITE = "princess"
PLAYER_DIR = "princess"
PLAYER_SPEED = 5
PLAYER_HEALTH = 200