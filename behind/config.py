import os


BASE_DIR = os.path.dirname(__file__)

SPRITE_DIRECTORY = os.path.join(BASE_DIR, 'assets', 'sprites')

# General Game configuration
GAME_WINDOW_WIDTH = 1280
GAME_WINDOW_HEIGHT = 720
GAME_WINDOW_TITLE = 'Behind the Scenes'
GAME_FPS = 60

# Player Configuration

# Set of sprites for the Player's different animation states
PLAYER_SPRITES = {
    'idle': {
        'name': 'player_standing',
        'directory': SPRITE_DIRECTORY,
    },
    'walking': {
        'name': 'player_running',
        'directory': SPRITE_DIRECTORY,
        'fps': 12,
    },
    'jumping': {
        'name': 'player_jumping',
        'directory': SPRITE_DIRECTORY,
        'fps': 6,
    },
    'damaged': {
        'name': '',
    },
    'killed': {
        'name': 'player_dying',
        'directory': SPRITE_DIRECTORY,
        'fps': 12,
    },
    'dead': {
        'name': 'player_dead',
        'directory': SPRITE_DIRECTORY,
    },
}

# Map player actions to keys
# Provide alternate keys to the same action by adding to the tuple
PLAYER_CONTROLS = {
    'left': ('left', 'a'),
    'right': ('right', 'd'),
    'jump': ('ctrl_left', 'ctrl_right', 'space'),
    'action': ('enter', 'f'),
}

# pixel/s
PLAYER_MOVE_SPEED = 200
PLAYER_JUMP_VELOCITY = -20
# pixel/s^2
GRAVITY = 1

# Background Configuration

# Set of sprites for the different scrolling backgrounds
BACKGROUND_SPRITES = {
    'front': {
        'name': 'front_scroll',
        'directory': SPRITE_DIRECTORY,
    },
    'behind': {
        'name': 'behind_scroll',
        'directory': SPRITE_DIRECTORY,
    },
}

# Platform Configuration
PLATFORM_SPRITES = {
    'left': {
        'name': 'platform_left',
        'directory': SPRITE_DIRECTORY,
    },
    'right': {
        'name': 'platform_right',
        'directory': SPRITE_DIRECTORY,
    },
    'middle': {
        'name': 'platform_middle',
        'directory': SPRITE_DIRECTORY,
    },
}

# Level Configuration
LEVELS = [
]
