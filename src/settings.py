from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
STATIC_PATH = BASE_PATH.joinpath('static')

FPS = 30 # (A) global var to determine refresh rate of the game
ROWS, COLS = 10, 10 # (A) how many blocks in the rows and cols will be used to calculate positionings (10x10 is standard battleship)
BLOCKHEIGHT, BLOCKWIDTH = 30, 30 # (A) height of each block for the board
GAMEHEIGHT, GAMEWIDTH = 700, 600 # (A) height/width of the actual game window
TURN_TIME_OUT_SECONDS = 3

SHIPCOLORS = {1: (255, 100, 100), 2: (100, 255, 100), 3: (100, 100, 255), 4: (255, 255, 100), 5: (255, 100, 255)} # (A) global colors for different type of ships

SOUNDS = {
    'explosion': STATIC_PATH.joinpath('sounds/explosion.mp3'),
    'missed': STATIC_PATH.joinpath('sounds/missed.mp3')
}
