import logging

import settings
import pygame
import sys
import random


from models import Player, AIGuessState


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


def drawBoard(player, enemy):  # (M) function that draws the board in the main game loop

    screen = getScreen()

    for x in range(settings.COLS):  # (A) iterate through each column
        for y in range(settings.ROWS):  # (A) iterate through each row as well to work with specific blocks of the matrix
            pyRect = (x * settings.BLOCKWIDTH + xOffset, y * settings.BLOCKHEIGHT + yOffset, settings.BLOCKWIDTH,
                      settings.BLOCKHEIGHT)  # (A) rectangle tuple that replaces a rectangle object with (x, y, width, height)

            should_highlight = False  # (A) variable to determine if we should highlight the current square in the loop
            if 0 <= hoverX < settings.COLS and 0 <= hoverY < settings.ROWS:  # (A) for one, it is mandatory to be within the board to even highlight
                if direction == 0 and hoverY == y and hoverX <= x < hoverX + currentShip and hoverX + currentShip <= settings.COLS:  # (A) now we figure out based on the direction (0 = right), is the currentNode covered by the path starting from the block the mouse points at
                    should_highlight = True  # (A) if direction == 0, then if node falls within the bounds of the path, (hoverX <= x < hoverX + currentShip) and also not out of bound (hoverX + currentShip <= COLS)
                elif direction == 1 and hoverX == x and hoverY <= y < hoverY + currentShip and hoverY + currentShip <= settings.ROWS:
                    should_highlight = True  # (A) similar logic to above, but direction == 1 is down, so check if y falls under that y path while not going out of bound
                elif direction == 2 and hoverY == y and hoverX - currentShip < x <= hoverX and hoverX - currentShip + 1 >= 0:  # (A) similar logic to above, direction 2 == left
                    should_highlight = True  # (A) one thing to note is that hoverY == y just means same row or same col depending on the direction of the path (if right, then col should be same)
                elif direction == 3 and hoverX == x and hoverY - currentShip < y <= hoverY and hoverY - currentShip + 1 >= 0:  # (A) similar logic to above, direction 3 == top
                    should_highlight = True

            if should_highlight:  # (A) if we should highlight this block
                pygame.draw.rect(screen, (155, 155, 155),
                                 pyRect)  # (A) then instead of a normal color we draw a gray block, but has a pink tone thanks to the background
            elif player.board[y][x] != 0:  # (A) if the block isn't even empty, e.g. it has a ship
                ship_size = player.board[y][
                    x]  # (A) find the type of ship/ship size by checking the player's board
                ship_color = settings.SHIPCOLORS.get(ship_size,
                                            (0, 255, 0))  # (A) get the color corresponding to the type of ship
                pygame.draw.rect(screen, ship_color, pyRect)  # (A) draw the block with the ship's color

            pygame.draw.rect(screen, lineColor, pyRect,
                             1)  # (A) this draws the grid, the extra parameter at the end determines if it's 'hollow' and has a border strength

    # print(hoverX, hoverY)
    pygame.display.flip()  # (A) then update the display so all the little color changes happen simutaneously

    for event in pygame.event.get():  # (A) listen for events in the game
        if event.type == pygame.QUIT:  # (A) if quit (x out) then quit the game
            pygame.quit()
        elif event.type == pygame.KEYDOWN:  # (A) pygame.KEYDOWN means that the user pressed down a key, nothing specific here
            if event.key == pygame.K_r:  # (A) specifically, if it is the R key (pygame.K_r) then rotate the ship by changing the direction
                direction = (direction + 1) % 4  # (A) this will just cycle within the (0-3) range by using modulo 4
        elif event.type == pygame.MOUSEBUTTONDOWN:  # (A) if the mouse was clicked
            if event.button == 1:  # (A) and the mouse click was the left click
                if 0 <= hoverX < settings.COLS and 0 <= hoverY < settings.ROWS:  # (A) first check the bounds of the click to make sure it was valid
                    if player.place_ship(hoverX, hoverY, currentShip,
                                         direction):  # (A) then see if you can place the ship within the player object's matrix
                        if ships:  # (A) if there are more ships to place
                            currentShip = ships.pop()  # (A) pop the next ship and repeat the loop
                        else:
                            waiting = False  # (A) break the loop otherwise


def drawBoard(player, enemy):  # (M) function that draws the board in the main game loop

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
            if player.guesses[y][x] == 'hit':  # (M) the guess was a hit
                pygame.draw.rect(screen, getPygameColor('ship-hit'), pyRect)  # (M) draw red on the spot for a hit
            elif player.guesses[y][x] == 'miss':  # (M) the guess was a miss
                pygame.draw.rect(screen, getPygameColor('ship-miss'), pyRect)  # (M) draw blue on the spot for a miss
            elif player.guesses[y][x] == 'sunk':  # (N) if the ship is sunk
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
            if player.board[y][x] != 0:
                ship_size = player.board[y][x]  # (M) get the type of ship from the player's board
                ship_image = settings.SHIPIMAGE.get(ship_size)  # (M) get the type of color from matching it to the global colors
                ship_image = pygame.transform.scale(ship_image, (settings.BLOCKHEIGHT, settings.BLOCKWIDTH)) #transforms the ship image to fit inside the square
                pygame.Surface.blit(screen, ship_image, pyRect) #Displays ship image to screen where player choses.
                # pygame.draw.rect(screen, ship_color, pyRect)  # (M) draw the colored square onto the board
            if enemy.guesses[y][x] != 0:  # (N) showing hits and misses on the player's own ships

                # (N) check through the enemy's guessses and mark spots as red, blue, or gray for hits, misses, and ships that are sunk respectively
                if enemy.guesses[y][x] == 'hit':
                    pygame.draw.rect(screen, getPygameColor('ship-hit'), pyRect)  # (N) hit means red
                elif enemy.guesses[y][x] == 'miss':  # (N) miss means blue
                    pygame.draw.rect(screen, getPygameColor('ship-miss'), pyRect)
                elif enemy.guesses[y][x] == 'sunk':  # (N) sunk means gray
                    pygame.draw.rect(screen, getPygameColor('ship-sunk'), pyRect)


def handleHit():

    screen = getScreen()

    hit_text = createText(
        'HIT! Please turn the screen to the next player',
        {
            'color': getPygameColor('ship-hit'),
        }
    )  # (N) essentially this is just a text fill on the screen that will indicate that it is a hit if the check_hit function returns True

    drawBackground()
    playSound('explosion')
    screen.blit(
        hit_text,
        (
            settings.GAMEWIDTH // 2 - hit_text.get_width() // 2,
            settings.GAMEHEIGHT // 2
        )
    )  # (N) display the hit text on the screen
    pygame.display.flip()  # (N) update display


def handleMiss():

    screen = getScreen()

    # (N) or if it was the miss do the exact same thing as for a hit but instead of "Hit" being displayed, put "Miss" instead
    miss_text = createText(
        'MISS! Please turn the screen to the next player',
        {
            'font-size': getFontSizePx('med'),
            'color': getPygameColor('ship-miss')
        }
    )

    drawBackground()
    playSound('missed')
    screen.blit(miss_text, (
        settings.GAMEWIDTH // 2 - miss_text.get_width() // 2,
        settings.GAMEHEIGHT // 2
    ))
    pygame.display.flip()


def handleWin(currentPlayer, enemy):

    screen = getScreen()

    # (N) display the current player # and that they have won the game
    winner_text = createText(
        f"Player {currentPlayer.num} Wins!",
        {
            'font-size': getFontSizePx('lg'),
            'color': (255, 0, 0)
        }
    )

    drawBackground()
    screen.blit(
        winner_text,
        (
            settings.GAMEWIDTH // 2 - winner_text.get_width() // 2,
            settings.GAMEHEIGHT // 2
        )
    )
    pygame.display.flip()
    pygame.time.wait(3000)  # (N) wait a bit
    return False


def handlePlayerTurn(currentPlayer, enemy):
    """  # (N) function that handles the current player's turn.
        When a click event happens on the guess board, check for a hit or miss and update board accordingly.
        Some code taken from ChatGPT but mostly changed to fix errors
    """

    screen = getScreen()

    waiting_for_input = True  # (A) wait for input so the screen doesn't instantly move
    x_offset = 150  # (N) setting virtical and horizontal offset to specify the guess board on top
    y_offset = 30

     # Define the Exit button for the top-right positioning
    button_width = 100
    button_height = 40
    margin = 30
    exit_button_rect = pygame.Rect((settings.GAMEWIDTH - button_width - margin, margin), (button_width, button_height))
    exit_font = pygame.font.Font(None, 24)
    exit_text = exit_font.render("Exit Game", True, (255, 255, 255))

    while waiting_for_input:  # (A) input waiting loop
        # (A) draw the board based on player/enemy data (top is guesses, bottom is player)
        drawBoard(currentPlayer, enemy)

 # Draw the exit button at the top right
        pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, 2)
        pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
        screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2,
                               exit_button_rect.centery - exit_text.get_height() // 2))

        pygame.display.flip()  # (A) update the screen with the rendered boards, and then wait for player to make a decision

        for event in pygame.event.get():  # (N) checking for events
            if event.type == pygame.QUIT:  # (N) if it is a quit event, return False meaning the game will end
                return False, None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:  # (N) if a click occurs
                if event.button == 1:
                    mouse_pos = event.pos
                    if exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    mouseX, mouseY = pygame.mouse.get_pos()  # (N) get the position of the mouse

                    # (N) looking for the specific position on the actual board
                    gridX = (mouseX - x_offset) // settings.BLOCKWIDTH
                    gridY = (mouseY - y_offset) // settings.BLOCKHEIGHT

                    if 0 <= gridX < settings.COLS and 0 <= gridY < settings.ROWS:  # (N) making sure the click is occuring on the guess board or it will not be inputted
                        if currentPlayer.guesses[gridY][gridX] == 0:  # (N) if the square hasn't been shot before
                            # (N) check if it was a hit or miss using the check_hit function
                            if currentPlayer.check_hit(enemy, gridX, gridY):
                               handleHit()
                            else:
                               handleMiss()
                            pygame.time.wait(settings.TURN_TIME_OUT_SECONDS * 1000)

                            # (N) redraw the board to show a hit or miss on the screen
                            drawBoard(currentPlayer, enemy)

                            # (N) check for a win by calling the function on the enemy, if that is the case and the current player has won
                            if check_for_win(enemy):
                                return handleWin(currentPlayer, enemy)

                            # (N) if the game isn't over just set waiting_for_input to be false so that the while loop ends
                            waiting_for_input = False

    return True


def handleMediumAITurn(ai_opponent: Player, player, ai_guess_state: AIGuessState):

    if ai_guess_state.on_a_roll: #If first was a hit 
        mouseX, mouseY = ai_guess_state.produce_guess() #Get a guess from algorithm 

        guess = None

        try:
            guess = ai_opponent.guesses[mouseY][mouseX] #Gets the passed guesses
        except IndexError:
            pass #if the next guess in algorithm is out of bounds Handles the excpetion

        if guess == 0: 
            #Checks to see if the AI hit the other players ships
            hit = ai_opponent.check_hit(player, mouseX, mouseY)
            #if number of sunk ships increaes then reset AI to random guess
            if ai_guess_state.curr_sunk_ships < player.count_sunk_ships():
                ai_guess_state.reset()
            elif hit:
                #If the next hit was a hit then continue with the guessing strategy 
                ai_guess_state.continue_roll((mouseX, mouseY))
            else:
                #if the hit was a miss then tally it as a bas gift 
                ai_guess_state.bad_guess((mouseX, mouseY))

            #Check if the player has won after the guess
            if check_for_win(player):
                return handleWin(ai_opponent, player)
        else:
            #Mark a miss as a bad guess
            ai_guess_state.bad_guess((mouseX, mouseY))
            #Calls function to handle medium ai difficulty 
            return handleMediumAITurn(ai_opponent, player, ai_guess_state)
        #returns true once the turn is complete 
        return True
    else:
        #updates the amount of sunk ships 
        ai_guess_state.curr_sunk_ships = player.count_sunk_ships()

        #Random positon for AI guess
        mouseX = random.randint(0, 9)
        mouseY = random.randint(0, 9)

        #Checks to see if the AI has guessed that position yet 
        if ai_opponent.guesses[mouseY][mouseX] == 0:
            #Checks to see if the guess was a hit 
            hit = ai_opponent.check_hit(player, mouseX, mouseY)

            if hit:
                #If it was a hit then start a roll 
                ai_guess_state.start_roll((mouseX, mouseY))

            #Checks to see if player won after guess
            if check_for_win(player):
                return handleWin(ai_opponent, player)
        else:
            #Handles the AI turn for medium 
            return handleMediumAITurn(ai_opponent, player, ai_guess_state)

        return True


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
