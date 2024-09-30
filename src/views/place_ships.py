
import pygame
import sys
import settings
from models import Player, PlayerTurn
from utils import drawLabels, createText, drawBackground, getScreen, getFontSizePx, getPygameColor


def show_place_ships(count, player):  # (A) startboard will have the user (current player) set up their board based on the count given

    screen = getScreen()
    lineColor = (255, 255, 255)  # (A) color for the grid/matrix lines; should be (255, 255, 255) or white
    yOffset = 150  # (A) offset to place the board in the middle of the game screen
    xOffset = 150  # (A) same offset but x-direction

    # (A) render the title, note it uses the player.num we initialized Player() with
    title = createText(f"Place Your Ships Player {player.num}",
    {
        'font-size': getFontSizePx('med'),
        'color': getPygameColor('start-menu-text')
    })
    instruction = createText(
    "Press R to rotate your placement. Click to place a ship.",
    {
        'font-size': getFontSizePx('xs'),
        'color': getPygameColor('start-menu-text')
    })  # (A) disclaimer on how to rotate and place ships

    # Define the Exit button for the top-right positioning
    button_width = 100
    button_height = 40
    margin = 30
    exit_button_rect = pygame.Rect((settings.GAMEWIDTH - button_width - margin, margin), (button_width, button_height))
    exit_font = pygame.font.Font(None, 24)
    exit_text = exit_font.render("Exit Game", True, getPygameColor('start-menu-text'))


    ships = [val + 1
             for val in
             range(count)]  # (A) rubric outlines each ship has a val of their count equivalent so [1,2,3.. etc.]
    currentShip = ships.pop()  # (A) we pop the last ship or highest value to start placements with
    direction = 0  # (A) direction by default is 0 which is right-facing

    waiting = True  # (A) function loop conditional so it doesn't instantly move away from this screen
    while waiting:  # (A) will wait for inputs
        drawBackground()
        screen.blit(title, (
            settings.GAMEWIDTH // 2 - title.get_width() // 2,
            yOffset - 75
        ))  # (A) push the rendered title to the top of the screen with screen.blit()
        screen.blit(instruction, (
            settings.GAMEWIDTH // 2 - instruction.get_width() // 2,
            yOffset + 315
        ))  # (A) same with the disclaimer, GAMEWIDTH // 2 - instruction.get_width() // 2 will just center the text

        # Draw the exit button at the top right
        pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, 2)
        pygame.draw.rect(screen, (141, 28, 22), exit_button_rect)
        screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2,
                               exit_button_rect.centery - exit_text.get_height() // 2))


        # (A) draw labels on the board as well for clarity, provide offsets to account for different scenarios
        drawLabels(xOffset, yOffset)
        mouseX, mouseY = pygame.mouse.get_pos()  # (A) pygame.mosue.get_pos() returns (x, y) of the mouse position
        hoverX = (mouseX - xOffset) // settings.BLOCKWIDTH  # (A) we disregard the part that the offset adds, then divide by WIDTH to take the board position (1-10)
        hoverY = (mouseY - yOffset) // settings.BLOCKHEIGHT  # (A) similar to above, we take the Y position that is normalized

        for x in range(settings.COLS):  # (A) iterate through each column
            for y in range(settings.ROWS):  # (A) iterate through each row as well to work with specific blocks of the matrix
                # (A) rectangle tuple that replaces a rectangle object with (x, y, width, height)
                pyRect = (
                    x * settings.BLOCKWIDTH + xOffset,
                    y * settings.BLOCKHEIGHT + yOffset,
                    settings.BLOCKWIDTH,
                    settings.BLOCKHEIGHT
                )

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
                    ship_image = settings.SHIPIMAGE.get(ship_size)  # (A) get the color corresponding to the type of ship
                    ship_image = pygame.transform.scale(ship_image, (settings.BLOCKHEIGHT, settings.BLOCKWIDTH)) #Transforms image to fit size of block
                    pygame.Surface.blit(screen, ship_image, pyRect) #Displays to board.s

                pygame.draw.rect(screen, lineColor, pyRect,
                                 1)  # (A) this draws the grid, the extra parameter at the end determines if it's 'hollow' and has a border strength

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
                    mouse_pos = event.pos
                    if exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
