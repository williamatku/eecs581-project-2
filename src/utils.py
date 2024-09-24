import settings
import pygame
import sys


def playSound(sound):
    """ plays a sound defined in settings.py """
    py_sound = settings.SOUNDS.get(sound)
    if py_sound is None:
        raise NotImplementedError(f'no sound defined in settings.py with name {sound}')
    else:
        pygame.mixer.Sound(py_sound).play()


def createText(font_size, text, color):
    py_font = settings.FONTS.get(font_size)
    if py_font is None:
        raise NotImplementedError(f'no font size defined in settings.py with name {font_size}')
    else:
        return (pygame.font
                .Font(py_font[0], py_font[1])
                .render(text, True, color)
                )


def drawLabels(screen, xOffset, yOffset):
    """ (M) function to just draw labels on the board as required by the rubric,
        offsets are so it does not collide with board
    """

    # (M) font object initialization, with a None reference to any existing font, and 26 as the size
    for i in range(settings.COLS):  # (M) for every column...
        # (M) have a font render itself on the screen, starting with chr(65+i) which starts as A
        label = createText('sm', chr(65 + i), (5, 5, 5))
        screen.blit(
            label,
            (
                xOffset + i * settings.BLOCKWIDTH + settings.BLOCKWIDTH // 2 - label.get_width() // 2,
                yOffset - 25
            )
        )  # (M) push this rendered font to the top of the screen, and space it out on the side with i * BLOCKWIDTH

    for i in range(settings.ROWS):  # (M) for every row...
        label = createText('sm', str(i + 1), (5, 5, 5))
        # (M) have the font render itself, this time just str() to convert the numbers into a string
        screen.blit(label, (xOffset - 25,
                            yOffset + i * settings.BLOCKHEIGHT + settings.BLOCKHEIGHT // 2 - label.get_height() // 2))  # (M) push again to the to pof the screen with blit and space it out with i * BLOCKHEIGHT


def drawBoard(screen, player, enemy):  # (M) function that draws the board in the main game loop
    lineColor = (255, 255, 255)  # (M) color of the lines
    topOffset = 30  # (M) offset we add so the column labels don't go off the screen for the top board
    bottomOffset = 400  # (M) bottom offset to push the bottom board down
    xOffset = 150  # (M) horizontal offset to center the boards

    drawLabels(screen, xOffset, topOffset)  # (M) draw labels on the top board
    for x in range(settings.COLS):  # (M) iterate through each column
        for y in range(settings.ROWS):  # (M) iterate through each row
            pyRect = (x * settings.BLOCKWIDTH + xOffset, y * settings.BLOCKHEIGHT + topOffset, settings.BLOCKWIDTH,
                      settings.BLOCKHEIGHT)  # (M) create a tuple for the rectangle object (x, y, width, height)
            pygame.draw.rect(screen, lineColor, pyRect, 1)  # (M) at the same time, we draw the grids for the board

            # (M) if the guess board does not have 0 at the guess matrix, it has one of 3 conditions
            if player.guesses[y][x] != 0:
                if player.guesses[y][x] == 'hit':  # (M) the guess was a hit
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)  # (M) draw red on the spot for a hit
                elif player.guesses[y][x] == 'miss':  # (M) the guess was a miss
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)  # (M) draw blue on the spot for a miss
                elif player.guesses[y][x] == 'sunk':  # (N) if the ship is sunk
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)  # (N) draw the spot as gray

    # (M) now draw the labels but on the bottom board, so we use bottom offset
    drawLabels(screen, xOffset, bottomOffset)

    for x in range(settings.COLS):  # (M) iterate through all the columns and rows again
        for y in range(settings.ROWS):
            pyRect = (x * settings.BLOCKWIDTH + xOffset, y * settings.BLOCKHEIGHT + bottomOffset, settings.BLOCKWIDTH,
                      settings.BLOCKHEIGHT)  # (M) same as above, we create a tuple for the rectangle (x, y, width, height)
            pygame.draw.rect(screen, lineColor, pyRect,
                             1)  # (M) and just like with the top board, draw the grids for the board

            # (M) since this is the player's board, we check the matrix to see if there are any ships at the spot
            if player.board[y][x] != 0:
                ship_size = player.board[y][x]  # (M) get the type of ship from the player's board
                ship_color = settings.SHIPCOLORS.get(ship_size, (
                0, 255, 0))  # (M) get the type of color from matching it to the global colors
                pygame.draw.rect(screen, ship_color, pyRect)  # (M) draw the colored square onto the board
            if enemy.guesses[y][x] != 0:  # (N) showing hits and misses on the player's own ships

                # (N) check through the enemy's guessses and mark spots as red, blue, or gray for hits, misses, and ships that are sunk respectively
                if enemy.guesses[y][x] == 'hit':
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)  # (N) hit means red
                elif enemy.guesses[y][x] == 'miss':  # (N) miss means blue
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)
                elif enemy.guesses[y][x] == 'sunk':  # (N) sunk means gray
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)


def handleHit(screen):
    hit_text = createText(
        'med',
        'HIT! Please turn the screen to the next player',
        (255, 0, 0)
    )  # (N) essentially this is just a text fill on the screen that will indicate that it is a hit if the check_hit function returns True
    screen.fill("skyblue")  # (N) fill screen with color bue
    playSound('explosion')
    screen.blit(
        hit_text,
        (
            settings.GAMEWIDTH // 2 - hit_text.get_width() // 2,
            settings.GAMEHEIGHT // 2
        )
    )  # (N) display the hit text on the screen
    pygame.display.flip()  # (N) update display


def handleMiss(screen):
    # (N) or if it was the miss do the exact same thing as for a hit but instead of "Hit" being displayed, put "Miss" instead
    miss_text = createText(
        'med',
        'MISS! Please turn the screen to the next player',
        (0, 0, 255)
    )
    screen.fill("skyblue")
    playSound('missed')
    screen.blit(miss_text, (settings.GAMEWIDTH // 2 - miss_text.get_width() // 2, settings.GAMEHEIGHT // 2))
    pygame.display.flip()


def handleWin(screen, currentPlayer, enemy):
    # (N) display the current player # and that they have won the game
    winner_text = createText(
        'lg',
        f"Player {currentPlayer.num} Wins!",
        (255, 0, 0)
    )
    screen.fill("skyblue")
    screen.blit(
        winner_text,
        (
            settings.GAMEWIDTH // 2 - winner_text.get_width() // 2,
            settings.GAMEHEIGHT // 2
        )
    )
    pygame.display.flip()
    pygame.time.wait(3000)  # (N) wait a bit
    return False, currentPlayer, enemy  # (N) then return False to end the game


def handlePlayerTurn(screen, currentPlayer, enemy):
    """  # (N) function that handles the current player's turn.
        When a click event happens on the guess board, check for a hit or miss and update board accordingly.
        Some code taken from ChatGPT but mostly changed to fix errors
    """
    waiting_for_input = True  # (A) wait for input so the screen doesn't instantly move
    x_offset = 150  # (N) setting virtical and horizontal offset to specify the guess board on top
    y_offset = 30
    while waiting_for_input:  # (A) input waiting loop
        # (A) draw the board based on player/enemy data (top is guesses, bottom is player)
        drawBoard(screen, currentPlayer, enemy)
        pygame.display.flip()  # (A) update the screen with the rendered boards, and then wait for player to make a decision

        for event in pygame.event.get():  # (N) checking for events
            if event.type == pygame.QUIT:  # (N) if it is a quit event, return False meaning the game will end
                return False, None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:  # (N) if a click occurs
                if event.button == 1:

                    mouseX, mouseY = pygame.mouse.get_pos()  # (N) get the position of the mouse

                    # (N) looking for the specific position on the actual board
                    gridX = (mouseX - x_offset) // settings.BLOCKWIDTH
                    gridY = (mouseY - y_offset) // settings.BLOCKHEIGHT

                    if 0 <= gridX < settings.COLS and 0 <= gridY < settings.ROWS:  # (N) making sure the click is occuring on the guess board or it will not be inputted
                        if currentPlayer.guesses[gridY][gridX] == 0:  # (N) if the square hasn't been shot before
                            # (N) check if it was a hit or miss using the check_hit function
                            if currentPlayer.check_hit(enemy, gridX, gridY):
                               handleHit(screen)
                            else:
                               handleMiss(screen)
                            pygame.time.wait(settings.TURN_TIME_OUT_SECONDS * 1000)

                            # (N) redraw the board to show a hit or miss on the screen
                            drawBoard(screen, currentPlayer, enemy)

                            # (N) check for a win by calling the function on the enemy, if that is the case and the current player has won
                            if check_for_win(enemy):
                                return handleWin(screen, currentPlayer, enemy)

                            # (N) if the game isn't over just set waiting_for_input to be false so that the while loop ends
                            waiting_for_input = False

    return True, currentPlayer, enemy  # (N) if the game isn't over, return true to keep the game going and swap the roles to make it the enemy's turn instead


def aiHardMode(screen, currentPlayer, enemy):
    drawBoard(screen, currentPlayer, enemy)


def check_for_win(player):
    """
        very quick function to check if the current player has won the game
        by looking at the enemy's ships that have been sunk to see if all of them have been sunk.
        Adapted from ChatGPT
    """

    # (N) this will check to see if all of the player's ships (which in the program is called as the enemy for the function call) are sunk.
    # (N) This is done by checking if every ship in the enemy's ships placed are present in their dicts of ships that are sunk. If that is the case then return true, otherwise return false because the game is not won yet
    return all(
        player.sunk_ships.get(ship_size, False)
        for ship_size in player.ships
    )
