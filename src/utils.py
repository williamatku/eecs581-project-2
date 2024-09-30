import logging

import settings
import pygame
import sys
import random


from models import Player, MediumAIGuessState


def playSound(sound):
    """ plays a sound defined in settings.py """
    py_sound = settings.SOUNDS.get(sound)
    if py_sound is None:
        raise NotImplementedError(f'no sound defined in settings.py with name {sound}')
    else:
        pygame.mixer.Sound(py_sound).play()


def getPygameColor(colorName):
    """ retrieves a color setting from settings.py """
    color = settings.COLORS.get(colorName)
    if color is None:
        raise NotImplementedError(f'no color defined in settings.py with name {colorName}')
    else:
        return color


def getFontSizePx(fontName):
    """ retrieves a font setting from settings.py """
    font = settings.FONT_SIZES.get(fontName)
    if font is None:
        raise NotImplementedError(f'no font size defined in settings.py with name {fontName}')
    else:
        return font


def createText(text, cust = {}):
    """ creates a pygame rendered text object from fonts defined in settings.py """

    # default text props
    font_size = cust.get('font-size') or getFontSizePx('med')
    color = cust.get('color') or getPygameColor('black')
    return (pygame.font
            .Font(None, font_size)
            .render(text, True, color)
            )


def getScreen():
    """ safely returns screen obj from pygame interface """
    screen = pygame.display.get_surface()
    if screen is None:
        raise NotImplementedError("Screen has not been initialized, cannot retrieve...")
    return screen


def drawBackground():
    getScreen().fill(getPygameColor('background'))


def display_fullscreen_message(message, options={}):

    screen = getScreen()

    # (N) or if it was the miss do the exact same thing as for a hit but instead of "Hit" being displayed, put "Miss" instead
    rendered_message = createText(
        message,
        options
    )

    drawBackground()
    playSound('missed')
    screen.blit(rendered_message, (
        settings.GAMEWIDTH // 2 - rendered_message.get_width() // 2,
        settings.GAMEHEIGHT // 2
    ))
    pygame.display.flip()


def drawLabels(xOffset, yOffset):
    """ (M) function to just draw labels on the board as required by the rubric,
        offsets are so it does not collide with board
    """

    screen = getScreen()

    # (M) font object initialization, with a None reference to any existing font, and 26 as the size
    for i in range(settings.COLS):  # (M) for every column...
        # (M) have a font render itself on the screen, starting with chr(65+i) which starts as A
        label = createText(chr(65 + i), {
            'font-size': getFontSizePx('sm'),
            'color': getPygameColor('start-menu-text')
        })
        screen.blit(
            label,
            (
                xOffset + i * settings.BLOCKWIDTH + settings.BLOCKWIDTH // 2 - label.get_width() // 2,
                yOffset - 25
            )
        )  # (M) push this rendered font to the top of the screen, and space it out on the side with i * BLOCKWIDTH

    for i in range(settings.ROWS):  # (M) for every row...
        label = createText(str(i + 1), {
            'font-size': getFontSizePx('sm'),
            'color': getPygameColor('start-menu-text')
        })
        # (M) have the font render itself, this time just str() to convert the numbers into a string
        screen.blit(label, (
            xOffset - 25,
            yOffset + i * settings.BLOCKHEIGHT + settings.BLOCKHEIGHT // 2 - label.get_height() // 2
        ))  # (M) push again to the to pof the screen with blit and space it out with i * BLOCKHEIGHT


def drawBoard(guesses_on_player_board, player_board, guesses_on_enemy_board):  # (M) function that draws the board in the main game loop

    screen = getScreen()

    lineColor = (255, 255, 255)  # (M) color of the lines
    topOffset = 30  # (M) offset we add so the column labels don't go off the screen for the top board
    bottomOffset = 400  # (M) bottom offset to push the bottom board down
    xOffset = 150  # (M) horizontal offset to center the boards

    drawLabels(xOffset, topOffset)  # (M) draw labels on the top board
    for x in range(settings.COLS):  # (M) iterate through each column
        for y in range(settings.ROWS):  # (M) iterate through each row
            # (M) create a tuple for the rectangle object (x, y, width, height)
            pyRect = (
                x * settings.BLOCKWIDTH + xOffset,
                y * settings.BLOCKHEIGHT + topOffset,
                settings.BLOCKWIDTH,
                settings.BLOCKHEIGHT
            )
            # (M) at the same time, we draw the grids for the board
            pygame.draw.rect(screen, lineColor, pyRect, 1)

            # (M) if the guess board does not have 0 at the guess matrix, it has one of 3 conditions
            if guesses_on_enemy_board[y][x] == 'hit':  # (M) the guess was a hit
                pygame.draw.rect(screen, getPygameColor('ship-hit'), pyRect)  # (M) draw red on the spot for a hit
            elif guesses_on_enemy_board[y][x] == 'miss':  # (M) the guess was a miss
                pygame.draw.rect(screen, getPygameColor('ship-miss'), pyRect)  # (M) draw blue on the spot for a miss
            elif guesses_on_enemy_board[y][x] == 'sunk':  # (N) if the ship is sunk
                pygame.draw.rect(screen, getPygameColor('ship-sunk'), pyRect)  # (N) draw the spot as gray

    # (M) now draw the labels but on the bottom board, so we use bottom offset
    drawLabels(xOffset, bottomOffset)

    for x in range(settings.COLS):  # (M) iterate through all the columns and rows again
        for y in range(settings.ROWS):
            # (M) same as above, we create a tuple for the rectangle (x, y, width, height)
            pyRect = (
                x * settings.BLOCKWIDTH + xOffset,
                y * settings.BLOCKHEIGHT + bottomOffset,
                settings.BLOCKWIDTH,
                settings.BLOCKHEIGHT
            )
            # (M) and just like with the top board, draw the grids for the board
            pygame.draw.rect(screen, lineColor, pyRect,1)

            # (M) since this is the player's board, we check the matrix to see if there are any ships at the spot
            if player_board[y][x] != 0:
                ship_size = player_board[y][x]  # (M) get the type of ship from the player's board
                ship_image = settings.SHIPIMAGE.get(ship_size)  # (M) get the type of color from matching it to the global colors
                ship_image = pygame.transform.scale(ship_image, (settings.BLOCKHEIGHT, settings.BLOCKWIDTH)) #transforms the ship image to fit inside the square
                pygame.Surface.blit(screen, ship_image, pyRect) #Displays ship image to screen where player choses.
                # pygame.draw.rect(screen, ship_color, pyRect)  # (M) draw the colored square onto the board

            # (N) check through the enemy's guessses and mark spots as red, blue, or gray for hits, misses, and ships that are sunk respectively
            if guesses_on_player_board[y][x] == 'hit':
                pygame.draw.rect(screen, getPygameColor('ship-hit'), pyRect)  # (N) hit means red
            elif guesses_on_player_board[y][x] == 'miss':  # (N) miss means blue
                pygame.draw.rect(screen, getPygameColor('ship-miss'), pyRect)
            elif guesses_on_player_board[y][x] == 'sunk':  # (N) sunk means gray
                pygame.draw.rect(screen, getPygameColor('ship-sunk'), pyRect)


def check_for_win(player):
    """
        very quick function to check if the current player has won the game
        by looking at the enemy's ships that have been sunk to see if all of them have been sunk.
        Adapted from ChatGPT
    """
   
    return all(
        player.sunk_ships.get(ship_size, False)
        for ship_size in player.ships
    )


def random_placement(count: int, ai_opponent: Player):

    placing = True

    ships = [val + 1
             for val in
             range(count)]  # (A) rubric outlines each ship has a val of their count equivalent so [1,2,3.. etc.]

    currentShip = ships.pop()  # (A) we pop the last ship or highest value to start placements with

    while placing:

        direction = random.randint(0, 3)
        placeX = random.randint(1, 10)
        placeY = random.randint(1, 10)

        if 0 <= placeX < settings.COLS and 0 <= placeY < settings.ROWS:  # (A) first check the bounds of the click to make sure it was valid
            if ai_opponent.place_ship(placeX, placeY, currentShip,
                                 direction):  # (A) then see if you can place the ship within the player object's matrix
                if ships:  # (A) if there are more ships to place
                    currentShip = ships.pop()  # (A) pop the next ship and repeat the loop
                else:
                    placing = False  # (A) break the loop otherwise


def handle_ai_win():
    display_fullscreen_message("The computer has prevailed, you lose", {
        'font-size': getFontSizePx('lg'),
        'color': getPygameColor('ship-hit')

    })
    pygame.time.wait(3_000)  # (N) wait a bit

