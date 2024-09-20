import pygame #importing required library

FPS = 30 # (A) global var to determine refresh rate of the game
ROWS, COLS = 10, 10 # (A) how many blocks in the rows and cols will be used to calculate positionings (10x10 is standard battleship)
BLOCKHEIGHT, BLOCKWIDTH = 30, 30 # (A) height of each block for the board
GAMEHEIGHT, GAMEWIDTH = 700, 600 # (A) height/width of the actual game window

SHIP1 = pygame.image.load('images/shipImages/shipSize1.png')
SHIP2 = pygame.image.load('images/shipImages/shipSize2.png')
SHIP3 = pygame.image.load('images/shipImages/shipSize3.png')
SHIP4 = pygame.image.load('images/shipImages/shipSize4.png')
SHIP5 = pygame.image.load('images/shipImages/shipSize5.png')

SHIPCOLORS = {1: SHIP1, 2: SHIP2, 3: SHIP3, 4: SHIP4, 5: SHIP5} # (A) global colors for different type of ships
