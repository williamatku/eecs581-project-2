import settings
import pygame

def getCount(screen):  # (M) initial screen that determines how many ships the players will deal with
    font = pygame.font.Font(None,
                            36)  # (M) setting the font is an initialization of pygame.font.Font(file, size) where file is if there's already a font type, and size is just the Size
    titleFont = pygame.font.Font(None,
                                 48)  # (M) need to initialize different fonts if we want different sizes for readaability
    smallFont = pygame.font.Font(None,
                                 24)  # (M) as above, these fonts will be used for different words/phrases and the size reflects that

    title = titleFont.render("Battleship", True, (5, 5, 5))  # (M) titleFont refers to the font initialized earlier
    prompt = font.render("How many ships would you like? (1-5)", True, (5, 5,
                                                                        5))  # (M) font.render(phrase, antialiasing, color, background) is self explanatory (background is not mandatory)
    startText = font.render("Press ENTER to start", True, (
    5, 5, 5))  # (M) by rendering, it's drawing these texts on the surface or "screen" we passed in earlier
    disclaimer = smallFont.render("Use the up and down arrows to adjust the # of ships", True, (5, 5, 5))

    ship_count = 1  # (M) minimum number of ships we can play with is one
    running = True  # (M) conditional for the game loop to continue

    while running:  # (M) this loop is necessary so the player can input their decisions without it going straight to the next screen
        screen.fill("skyblue")  # (M) fill the background with skyblue

        screen.blit(title, (settings.GAMEWIDTH // 2 - title.get_width() // 2,
                            100))  # (M) place a rendered object on top of the screen, in this case our texts
        screen.blit(prompt, (settings.GAMEWIDTH // 2 - prompt.get_width() // 2,
                             200))  # (M) this will make the texts visible, and takes in x, y parameters
        screen.blit(startText, (settings.GAMEWIDTH // 2 - startText.get_width() // 2,
                                400))  # (M) GAMEWIDTH // 2 - text.get_width() // 2 helps center in the horizontal plane
        screen.blit(startText, (settings.GAMEWIDTH // 2 - startText.get_width() // 2,
                                400))  # (M) vertical placement is subjective, so we just pick whatever looks appealing
        screen.blit(disclaimer,
                    (settings.GAMEWIDTH // 2 - disclaimer.get_width() // 2, 450))  # (M) placing another text onto the screen

        count_text = font.render(str(ship_count), True, (5, 5,
                                                         5))  # (M) new text to render inside the loop because it's dependent on the count of what the user has chosen
        screen.blit(count_text, (settings.GAMEWIDTH // 2 - count_text.get_width() // 2,
                                 300))  # (M) we will still need to place this to the top of the screen

        pygame.display.flip()  # (M) pygame.display.flip() will update the screen with the newly placed objects

        for event in pygame.event.get():  # (M) gameplay loop for listening to inputs within the game
            if event.type == pygame.QUIT:  # (M) if you close out, this is a pygame.QUIT event and ends the screen/game
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # (M) keydown refers to the act of pushing any key down, not just the down key
                if event.key == pygame.K_UP:  # (M) if this is going up, then user wants more ships
                    ship_count = min(ship_count + 1,
                                     5)  # (M) however, max count is 5, so if the user wants more than 5, just take the 5 which will be the min
                elif event.key == pygame.K_DOWN:  # (M) likewise if this goes down, the user wants less ships
                    ship_count = max(ship_count - 1, 1)  # (M) but ship count is lower bound by 1
                elif event.key == pygame.K_RETURN:  # (M) if user presses enter, then we are good to send the ship count back
                    return ship_count  # (M) this allows for the shipcount to be sent back to main() and get used by game for selection and gameplay

    return ship_count  # (M) if the running is broken in any way, default is 1


def drawLabels(screen, xOffset,
               yOffset):  # (M) function to just draw labels on the board as required by the rubric, offsets are so it does not collide with board
    font = pygame.font.Font(None,
                            26)  # (M) font object initialization, with a None reference to any existing font, and 26 as the size
    for i in range(settings.COLS):  # (M) for every column...
        label = font.render(chr(65 + i), True, (
        5, 5, 5))  # (M) have a font render itself on the screen, starting with chr(65+i) which starts as A
        screen.blit(label, (xOffset + i * settings.BLOCKWIDTH + settings.BLOCKWIDTH // 2 - label.get_width() // 2,
                            yOffset - 25))  # (M) push this rendered font to the top of the screen, and space it out on the side with i * BLOCKWIDTH

    for i in range(settings.ROWS):  # (M) for every row...
        label = font.render(str(i + 1), True, (
        5, 5, 5))  # (M) have the font render itself, this time just str() to convert the numbers into a string
        screen.blit(label, (xOffset - 25,
                            yOffset + i * settings.BLOCKHEIGHT + settings.BLOCKHEIGHT // 2 - label.get_height() // 2))  # (M) push again to the to pof the screen with blit and space it out with i * BLOCKHEIGHT


def startBoard(screen, count,
               player):  # (A) startboard will have the user (current player) set up their board based on the count given
    lineColor = (255, 255, 255)  # (A) color for the grid/matrix lines; should be (255, 255, 255) or white
    yOffset = 150  # (A) offset to place the board in the middle of the game screen
    xOffset = 150  # (A) same offset but x-direction

    font = pygame.font.Font(None, 36)  # (A) create a font object with 36 size font
    smallFont = pygame.font.Font(None, 16)  # (A) create another font object but with 16 for small disclaimers
    title = font.render(f"Place Your Ships Player {player.num}", True,
                        (5, 5, 5))  # (A) render the title, note it uses the player.num we initialized Player() with
    instruction = smallFont.render("Press R to rotate your placement. Click to place a ship.", True,
                                   (5, 5, 5))  # (A) disclaimer on how to rotate and place ships

    ships = [val + 1 for val in
             range(count)]  # (A) rubric outlines each ship has a val of their count equivalent so [1,2,3.. etc.]
    currentShip = ships.pop()  # (A) we pop the last ship or highest value to start placements with
    direction = 0  # (A) direction by default is 0 which is right-facing

    waiting = True  # (A) function loop conditional so it doesn't instantly move away from this screen
    while waiting:  # (A) will wait for inputs
        screen.fill("skyblue")  # (A) background will be skyblue
        screen.blit(title, (settings.GAMEWIDTH // 2 - title.get_width() // 2,
                            yOffset - 75))  # (A) push the rendered title to the top of the screen with screen.blit()
        screen.blit(instruction, (settings.GAMEWIDTH // 2 - instruction.get_width() // 2,
                                  yOffset + 315))  # (A) same with the disclaimer, GAMEWIDTH // 2 - instruction.get_width() // 2 will just center the text

        drawLabels(screen, xOffset,
                   yOffset)  # (A) draw labels on the board as well for clarity, provide offsets to account for different scenarios

        mouseX, mouseY = pygame.mouse.get_pos()  # (A) pygame.mosue.get_pos() returns (x, y) of the mouse position
        hoverX = (
                             mouseX - xOffset) // settings.BLOCKWIDTH  # (A) we disregard the part that the offset adds, then divide by WIDTH to take the board position (1-10)
        hoverY = (mouseY - yOffset) // settings.BLOCKHEIGHT  # (A) similar to above, we take the Y position that is normalized

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
                    ship_image = settings.SHIPCOLORS.get(ship_size)  # (A) get the color corresponding to the type of ship
                    ship_image = pygame.transform.scale(ship_image, (settings.BLOCKHEIGHT, settings.BLOCKWIDTH)) #Scaling the image to size of game tiles
                    pygame.Surface.blit(screen, ship_image, pyRect) #Places ship where user choses.
                    # pygame.draw.rect(screen, ship_color, pyRect)  # (A) draw the block with the ship's color

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
            if player.guesses[y][
                x] != 0:  # (M) if the guess board does not have 0 at the guess matrix, it has one of 3 conditions
                if player.guesses[y][x] == 'hit':  # (M) the guess was a hit
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)  # (M) draw red on the spot for a hit
                elif player.guesses[y][x] == 'miss':  # (M) the guess was a miss
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)  # (M) draw blue on the spot for a miss
                elif player.guesses[y][x] == 'sunk':  # (N) if the ship is sunk
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)  # (N) draw the spot as gray

    drawLabels(screen, xOffset,
               bottomOffset)  # (M) now draw the labels but on the bottom board, so we use bottom offset
    for x in range(settings.COLS):  # (M) iterate through all the columns and rows again
        for y in range(settings.ROWS):
            pyRect = (x * settings.BLOCKWIDTH + xOffset, y * settings.BLOCKHEIGHT + bottomOffset, settings.BLOCKWIDTH,
                      settings.BLOCKHEIGHT)  # (M) same as above, we create a tuple for the rectangle (x, y, width, height)
            pygame.draw.rect(screen, lineColor, pyRect,
                             1)  # (M) and just like with the top board, draw the grids for the board
            if player.board[y][
                x] != 0:  # (M) since this is the player's board, we check the matrix to see if there are any ships at the spot
                ship_size = player.board[y][x]  # (M) get the type of ship from the player's board
                ship_image = settings.SHIPCOLORS.get(ship_size)  # (M) get the type of color from matching it to the global colors
                ship_image = pygame.transform.scale(ship_image, (settings.BLOCKHEIGHT, settings.BLOCKWIDTH)) #transforms the ship image to fit inside the square
                pygame.Surface.blit(screen, ship_image, pyRect) #Displays ship image to screen where player choses.
                # pygame.draw.rect(screen, ship_color, pyRect)  # (M) draw the colored square onto the board
            if enemy.guesses[y][x] != 0:  # (N) showing hits and misses on the player's own ships
                if enemy.guesses[y][
                    x] == 'hit':  # (N) check through the enemy's guessses and mark spots as red, blue, or gray for hits, misses, and ships that are sunk respectively
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)  # (N) hit means red
                elif enemy.guesses[y][x] == 'miss':  # (N) miss means blue
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)
                elif enemy.guesses[y][x] == 'sunk':  # (N) sunk means gray
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)


def handlePlayerTurn(screen, currentPlayer,
                     enemy):  # (N) function that handles the current player's turn. When a click event happens on the guess board, check for a hit or miss and update board accordingly. Some code taken from ChatGPT but mostly changed to fix errors
    waiting_for_input = True  # (A) wait for input so the screen doesn't instantly move
    x_offset = 150  # (N) setting virtical and horizontal offset to specify the guess board on top
    y_offset = 30
    font = pygame.font.Font(None, 36)  # (N) just a font to use when text will be displayed
    while waiting_for_input:  # (A) input waiting loop
        drawBoard(screen, currentPlayer,
                  enemy)  # (A) draw the board based on player/enemy data (top is guesses, bottom is player)
        pygame.display.flip()  # (A) update the screen with the rendered boards, and then wait for player to make a decision

        for event in pygame.event.get():  # (N) checking for events
            if event.type == pygame.QUIT:  # (N) if it is a quit event, return False meaning the game will end
                return False, None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:  # (N) if a click occurs
                if event.button == 1:

                    mouseX, mouseY = pygame.mouse.get_pos()  # (N) get the position of the mouse

                    gridX = (
                                        mouseX - x_offset) // settings.BLOCKWIDTH  # (N) looking for the specific position on the actual board
                    gridY = (mouseY - y_offset) // settings.BLOCKHEIGHT

                    if 0 <= gridX < settings.COLS and 0 <= gridY < settings.ROWS:  # (N) making sure the click is occuring on the guess board or it will not be inputted
                        if currentPlayer.guesses[gridY][gridX] == 0:  # (N) if the square hasn't been shot before
                            if currentPlayer.check_hit(enemy, gridX,
                                                       gridY):  # (N) check if it was a hit or miss using the check_hit function
                                hit_text = font.render(f"Hit", True, (255, 0,
                                                                      0))  # (N) essentially this is just a text fill on the screen that will indicate that it is a hit if the check_hit function returns True
                                screen.fill("skyblue")  # (N) fill screen with color bue
                                screen.blit(hit_text, (settings.GAMEWIDTH // 2 - hit_text.get_width() // 2,
                                                       settings.GAMEHEIGHT // 2))  # (N) display the hit text on the screen
                                pygame.display.flip()  # (N) update display
                                pygame.time.wait(500)  # (N) wait a bit so the hit shows for a little bit
                            else:
                                miss_text = font.render(f"Miss", True, (0, 0,
                                                                        255))  # (N) or if it was the miss do the exact same thing as for a hit but instead of "Hit" being displayed, put "Miss" instead
                                screen.fill("skyblue")
                                screen.blit(miss_text, (settings.GAMEWIDTH // 2 - miss_text.get_width() // 2, settings.GAMEHEIGHT // 2))
                                pygame.display.flip()
                                pygame.time.wait(500)
                            drawBoard(screen, currentPlayer,
                                      enemy)  # (N) redraw the board to show a hit or miss on the screen
                            if check_for_win(
                                    enemy):  # (N) check for a win by calling the function on the enemy, if that is the case and the current player has won
                                font = pygame.font.Font(None,
                                                        48)  # (N) display the current player # and that they have won the game
                                winner_text = font.render(f"Player {currentPlayer.num} Wins!", True, (255, 0, 0))
                                screen.fill("skyblue")
                                screen.blit(winner_text,
                                            (settings.GAMEWIDTH // 2 - winner_text.get_width() // 2, settings.GAMEHEIGHT // 2))
                                pygame.display.flip()
                                pygame.time.wait(3000)  # (N) wait a bit
                                return False, currentPlayer, enemy  # (N) then return False to end the game
                            waiting_for_input = False  # (N) if the game isn't over just set waiting_for_input to be false so that the while loop ends

    return True, currentPlayer, enemy  # (N) if the game isn't over, return true to keep the game going and swap the roles to make it the enemy's turn instead


def check_for_win(
        player):  # (N) very quick function to check if the current player has won the game by looking at the enemy's ships that have been sunk to see if all of them have been sunk. Adapted from ChatGPT
    return all(player.sunk_ships.get(ship_size, False) for ship_size in
               player.ships)  # (N) this will check to see if all of the player's ships (which in the program is called as the enemy for the function call) are sunk.
    # (N) This is done by checking if every ship in the enemy's ships placed are present in their dicts of ships that are sunk. If that is the case then return true, otherwise return false because the game is not won yet
