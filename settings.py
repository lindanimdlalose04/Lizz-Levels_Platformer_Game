"""Shared constants, asset loading and small helpers for Lizz Levels.

Everything that the rest of the game needs to agree on lives here, so the
numbers are in one place instead of scattered through the code.
"""

import os

import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'img')
SAVE_FILE = os.path.join(BASE_DIR, 'savegame.json')

# the world is a fixed grid, one screen per level
TILE_SIZE = 50
COLS = 20
ROWS = 20
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE
FPS = 60

# player physics. a jump of -16 with gravity 1 rises 136px, which clears a
# two tile step (100px) and carries about three tiles sideways, so every
# level is designed inside those limits
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 80
PLAYER_SPEED = 5
JUMP_VELOCITY = -16
GRAVITY = 1
MAX_FALL_SPEED = 10
DEATH_VELOCITY = -14
START_LIVES = 3

# platforms are drawn half a tile thick but collide on a thinner band at the
# top. a tile is 50px and the player is 80px tall, so a 25px band two rows up
# would clip a standing player on the head. 12px leaves 8px of clearance.
PLATFORM_THICKNESS = TILE_SIZE // 4

# moving platforms travel this far from where they start, in each direction
PLATFORM_TRAVEL = 2 * TILE_SIZE
PLATFORM_SPEED = 2
# how close a falling player must be to a platform top to count as landing
PLATFORM_TOLERANCE = 14

GHOST_SPEED = 1
GHOST_TRAVEL = 3 * TILE_SIZE
GHOST_ALPHA = 185

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CREAM = (255, 246, 214)
GOLD = (255, 200, 60)
RED = (220, 60, 60)
GREEN = (120, 220, 130)
SHADOW = (20, 20, 30)


def load_image(name, size=None, alpha=True):
    """Load an image from img/ and optionally scale it."""
    image = pygame.image.load(os.path.join(IMG_DIR, name))
    image = image.convert_alpha() if alpha else image.convert()
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image


def load_font(size):
    """Pick the nicest available font, falling back to pygame's default."""
    for name in ('bauhaus93', 'trebuchetms', 'verdana', 'arial'):
        path = pygame.font.match_font(name)
        if path:
            return pygame.font.Font(path, size)
    return pygame.font.Font(None, size)


def load_assets():
    """Load every image once. Must be called after the display is created."""
    tile = (TILE_SIZE, TILE_SIZE)
    half = (TILE_SIZE, TILE_SIZE // 2)
    ghost = load_image('ghost.png', (int(TILE_SIZE * 0.9), int(TILE_SIZE * 0.9)))
    ghost.set_alpha(GHOST_ALPHA)
    player_frames = [
        load_image('guy%d.png' % n, (PLAYER_WIDTH, PLAYER_HEIGHT))
        for n in range(1, 5)
    ]
    return {
        'dirt': load_image('dirt.png', tile),
        'grass': load_image('grass.png', tile),
        'lava': load_image('lava.png', half),
        'platform': load_image('platform.png', half),
        'platform_x': load_image('platform_x.png', half),
        'platform_y': load_image('platform_y.png', half),
        'coin': load_image('coin.png', (25, 25)),
        'coin_hud': load_image('coin.png', (32, 32)),
        'exit': load_image('exit.png', (TILE_SIZE, int(TILE_SIZE * 1.5))),
        'blob': load_image('blob.png', (TILE_SIZE, int(TILE_SIZE * 0.7))),
        'ghost': ghost,
        'player_frames': player_frames,
        'life': load_image('guy1.png', (22, 42)),
        'sky': load_image('sky.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), alpha=False),
        'sky_ruins': load_image('skyOLD.png', (SCREEN_WIDTH, SCREEN_HEIGHT), alpha=False),
        'start_btn': load_image('start_btn.png'),
        'exit_btn': load_image('exit_btn.png'),
        'restart_btn': load_image('restart_btn.png', (240, 84)),
        'save_btn': load_image('save_btn.png', (160, 84)),
        'load_btn': load_image('load_btn.png', (160, 84)),
    }


def load_sounds():
    """Load the sound effects. Returns an empty dict if there is no audio device."""
    try:
        return {
            'jump': pygame.mixer.Sound(os.path.join(IMG_DIR, 'jump.wav')),
            'coin': pygame.mixer.Sound(os.path.join(IMG_DIR, 'coin.wav')),
            'game_over': pygame.mixer.Sound(os.path.join(IMG_DIR, 'game_over.wav')),
        }
    except pygame.error:
        return {}
