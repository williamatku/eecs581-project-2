
import pygame

import settings
from models import Player, PlayerTurn
from utils import drawLabels


def showStartMenu(screen):  # (M) initial screen that determines how many ships the players will deal with
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

def showInitialGameView(screen, count,
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


def showAIModeSelection(screen):
    # Fonts for the buttons
    font = pygame.font.Font(None, 36)

    # Text for the buttons
    ai_text = font.render("PVC", True, (255, 255, 255))  # White text for better contrast
    player_text = font.render("PVP", True, (255, 255, 255))

    # Button dimensions and positions
    button_width = 300
    button_height = 60
    ai_button_rect = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 200), (button_width, button_height))
    player_button_rect = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 300), (button_width, button_height))

    running = True
    while running:
        screen.fill("skyblue")  # Clear screen with sky blue background

        # Add shadow effect for the buttons
        shadow_offset = 5
        pygame.draw.rect(screen, (0, 100, 0), ai_button_rect.move(shadow_offset, shadow_offset), border_radius=10)
        pygame.draw.rect(screen, (0, 100, 0), player_button_rect.move(shadow_offset, shadow_offset), border_radius=10)

        # Draw the buttons with rounded corners
        pygame.draw.rect(screen, (0, 200, 0), ai_button_rect, border_radius=10)  # Rounded corners with border_radius
        pygame.draw.rect(screen, (0, 200, 0), player_button_rect, border_radius=10)

        # Draw the text on the buttons
        screen.blit(ai_text, (
        ai_button_rect.centerx - ai_text.get_width() // 2, ai_button_rect.centery - ai_text.get_height() // 2))
        screen.blit(player_text, (player_button_rect.centerx - player_text.get_width() // 2,
                                  player_button_rect.centery - player_text.get_height() // 2))

        pygame.display.flip()  # Update screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # Check if clicked on AI button
                if ai_button_rect.collidepoint(mouse_pos):
                    print("AI mode selected")  # Placeholder until AI functionality is complete
                    running = False
                    return "AI"

                # Check if clicked on Play Against Player button
                if player_button_rect.collidepoint(mouse_pos):
                    print("Player mode selected")
                    running = False
                    return "Player"



def showTurnTransitionScreen(screen, pturn: PlayerTurn):
    # Fonts for the buttons
    font = pygame.font.Font(None, 36)

    # Text for the buttons
    question_text = font.render(f"Player {pturn}, are you ready?", True, (255, 255, 255))  # White text for better contrast
    confirm_button_text = font.render("Lets Battle", True, (255, 255, 255))

    # Button dimensions and positions
    button_width = 300
    button_height = 60

    confirm_button = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 300), (button_width, button_height))

    running = True
    while running:
        screen.fill("skyblue")  # Clear screen with sky blue background

        # Add shadow effect for the buttons
        shadow_offset = 5
        pygame.draw.rect(screen, (0, 100, 0), confirm_button.move(shadow_offset, shadow_offset), border_radius=10)

        # Draw the buttons with rounded corners
        pygame.draw.rect(screen, (0, 200, 0), confirm_button, border_radius=10)

        # Draw the text on the buttons
        screen.blit(question_text, (
            settings.GAMEWIDTH // 2 - question_text.get_width() // 2,
            100
        ))
        screen.blit(confirm_button_text, (
            confirm_button.centerx - question_text.get_width() // 2,
            confirm_button.centery - question_text.get_height() // 2
        ))

        pygame.display.flip()  # Update screen

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                mouse_pos = event.pos
                # Check if clicked on AI button
                if confirm_button.collidepoint(mouse_pos):
                    print("Clicked")
                    return
