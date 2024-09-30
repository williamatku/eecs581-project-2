from pathlib import Path
import pygame

BASE_PATH = Path(__file__).resolve().parent.parent
STATIC_PATH = BASE_PATH.joinpath('static')

FPS = 30 # (A) global var to determine refresh rate of the game
ROWS, COLS = 10, 10 # (A) how many blocks in the rows and cols will be used to calculate positionings (10x10 is standard battleship)
BLOCKHEIGHT, BLOCKWIDTH = 30, 30 # (A) height of each block for the board
GAMEHEIGHT, GAMEWIDTH = 700, 600 # (A) height/width of the actual game window
TURN_TIME_OUT_SECONDS = 3

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'background': (59, 65, 57),
    'start-menu-text': (224, 227, 223),
    'start-menu-text-2': (139, 151, 135),
    'ship-hit': (255, 0, 0),
    'ship-miss': (0, 0, 255),
    'ship-sunk': (0, 0, 0)
}

SHIP1 = pygame.image.load(STATIC_PATH.joinpath('images/shipImages/shipSize1.png'))
SHIP2 = pygame.image.load(STATIC_PATH.joinpath('images/shipImages/shipSize2.png'))
SHIP3 = pygame.image.load(STATIC_PATH.joinpath('images/shipImages/shipSize3.png'))
SHIP4 = pygame.image.load(STATIC_PATH.joinpath('images/shipImages/shipSize4.png'))
SHIP5 = pygame.image.load(STATIC_PATH.joinpath('images/shipImages/shipSize5.png'))

SHIPIMAGE = {1: SHIP1, 2: SHIP2, 3: SHIP3, 4: SHIP4, 5: SHIP5} # (A) global colors for different type of ships

SOUNDS = {
    'explosion': STATIC_PATH.joinpath('sounds/explosion.mp3'),
    'missed': STATIC_PATH.joinpath('sounds/missed.mp3')
}

FONT_SIZES = {
    'xs': 16,
    'sm': 26,
    'med': 36,
    'lg': 48,
}
