import settings
import pygame
import sys

def getCount(screen):  # (M) initial screen that determines how many ships the players will deal with
    font = pygame.font.Font(None, 36)
    titleFont = pygame.font.Font(None, 48)
    smallFont = pygame.font.Font(None, 24)

    title = titleFont.render("Battleship", True, (5, 5, 5))
    prompt = font.render("How many ships would you like? (1-5)", True, (5, 5, 5))
    startText = font.render("Press ENTER to start", True, (5, 5, 5))
    disclaimer = smallFont.render("Use the up and down arrows to adjust the # of ships", True, (5, 5, 5))

    ship_count = 1
    running = True

    while running:
        screen.fill("skyblue")

        screen.blit(title, (settings.GAMEWIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(prompt, (settings.GAMEWIDTH // 2 - prompt.get_width() // 2, 200))
        screen.blit(startText, (settings.GAMEWIDTH // 2 - startText.get_width() // 2, 400))
        screen.blit(disclaimer, (settings.GAMEWIDTH // 2 - disclaimer.get_width() // 2, 450))

        count_text = font.render(str(ship_count), True, (5, 5, 5))
        screen.blit(count_text, (settings.GAMEWIDTH // 2 - count_text.get_width() // 2, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ship_count = min(ship_count + 1, 5)
                elif event.key == pygame.K_DOWN:
                    ship_count = max(ship_count - 1, 1)
                elif event.key == pygame.K_RETURN:
                    return ship_count

    return ship_count


def drawLabels(screen, xOffset, yOffset):
    font = pygame.font.Font(None, 26)
    for i in range(settings.COLS):
        label = font.render(chr(65 + i), True, (5, 5, 5))
        screen.blit(label, (xOffset + i * settings.BLOCKWIDTH + settings.BLOCKWIDTH // 2 - label.get_width() // 2, yOffset - 25))

    for i in range(settings.ROWS):
        label = font.render(str(i + 1), True, (5, 5, 5))
        screen.blit(label, (xOffset - 25, yOffset + i * settings.BLOCKHEIGHT + settings.BLOCKHEIGHT // 2 - label.get_height() // 2))


def startBoard(screen, count, player):
    lineColor = (255, 255, 255)
    yOffset = 150
    xOffset = 150

    font = pygame.font.Font(None, 36)
    smallFont = pygame.font.Font(None, 16)
    title = font.render(f"Place Your Ships Player {player.num}", True, (5, 5, 5))
    instruction = smallFont.render("Press R to rotate your placement. Click to place a ship.", True, (5, 5, 5))

    ships = [val + 1 for val in range(count)]
    currentShip = ships.pop()
    direction = 0

    waiting = True
    while waiting:
        screen.fill("skyblue")
        screen.blit(title, (settings.GAMEWIDTH // 2 - title.get_width() // 2, yOffset - 75))
        screen.blit(instruction, (settings.GAMEWIDTH // 2 - instruction.get_width() // 2, yOffset + 315))

        drawLabels(screen, xOffset, yOffset)

        mouseX, mouseY = pygame.mouse.get_pos()
        hoverX = (mouseX - xOffset) // settings.BLOCKWIDTH
        hoverY = (mouseY - yOffset) // settings.BLOCKHEIGHT

        for x in range(settings.COLS):
            for y in range(settings.ROWS):
                pyRect = (x * settings.BLOCKWIDTH + xOffset, y * settings.BLOCKHEIGHT + yOffset, settings.BLOCKWIDTH, settings.BLOCKHEIGHT)

                should_highlight = False
                if 0 <= hoverX < settings.COLS and 0 <= hoverY < settings.ROWS:
                    if direction == 0 and hoverY == y and hoverX <= x < hoverX + currentShip and hoverX + currentShip <= settings.COLS:
                        should_highlight = True
                    elif direction == 1 and hoverX == x and hoverY <= y < hoverY + currentShip and hoverY + currentShip <= settings.ROWS:
                        should_highlight = True
                    elif direction == 2 and hoverY == y and hoverX - currentShip < x <= hoverX and hoverX - currentShip + 1 >= 0:
                        should_highlight = True
                    elif direction == 3 and hoverX == x and hoverY - currentShip < y <= hoverY and hoverY - currentShip + 1 >= 0:
                        should_highlight = True

                if should_highlight:
                    pygame.draw.rect(screen, (155, 155, 155), pyRect)
                elif player.board[y][x] != 0:
                    ship_size = player.board[y][x]
                    ship_color = settings.SHIPCOLORS.get(ship_size, (0, 255, 0))
                    pygame.draw.rect(screen, ship_color, pyRect)

                pygame.draw.rect(screen, lineColor, pyRect, 1)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    direction = (direction + 1) % 4
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 0 <= hoverX < settings.COLS and 0 <= hoverY < settings.ROWS:
                        if player.place_ship(hoverX, hoverY, currentShip, direction):
                            if ships:
                                currentShip = ships.pop()
                            else:
                                waiting = False


def drawBoard(screen, player, enemy):
    lineColor = (255, 255, 255)
    topOffset = 30
    bottomOffset = 400
    xOffset = 150

    drawLabels(screen, xOffset, topOffset)
    for x in range(settings.COLS):
        for y in range(settings.ROWS):
            pyRect = (x * settings.BLOCKWIDTH + xOffset, y * settings.BLOCKHEIGHT + topOffset, settings.BLOCKWIDTH, settings.BLOCKHEIGHT)
            pygame.draw.rect(screen, lineColor, pyRect, 1)
            if player.guesses[y][x] != 0:
                if player.guesses[y][x] == 'hit':
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)
                elif player.guesses[y][x] == 'miss':
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)
                elif player.guesses[y][x] == 'sunk':
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)

    drawLabels(screen, xOffset, bottomOffset)
    for x in range(settings.COLS):
        for y in range(settings.ROWS):
            pyRect = (x * settings.BLOCKWIDTH + xOffset, y * settings.BLOCKHEIGHT + bottomOffset, settings.BLOCKWIDTH, settings.BLOCKHEIGHT)
            pygame.draw.rect(screen, lineColor, pyRect, 1)
            if player.board[y][x] != 0:
                ship_size = player.board[y][x]
                ship_color = settings.SHIPCOLORS.get(ship_size, (0, 255, 0))
                pygame.draw.rect(screen, ship_color, pyRect)
            if enemy.guesses[y][x] != 0:
                if enemy.guesses[y][x] == 'hit':
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)
                elif enemy.guesses[y][x] == 'miss':
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)
                elif enemy.guesses[y][x] == 'sunk':
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)


def handlePlayerTurn(screen, currentPlayer, enemy):
    waiting_for_input = True
    x_offset = 150
    y_offset = 30
    font = pygame.font.Font(None, 36)
    while waiting_for_input:
        drawBoard(screen, currentPlayer, enemy)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    mouseX, mouseY = pygame.mouse.get_pos()

                    gridX = (mouseX - x_offset) // settings.BLOCKWIDTH
                    gridY = (mouseY - y_offset) // settings.BLOCKHEIGHT

                    if 0 <= gridX < settings.COLS and 0 <= gridY < settings.ROWS:
                        if currentPlayer.guesses[gridY][gridX] == 0:
                            if currentPlayer.check_hit(enemy, gridX, gridY):
                                hit_text = font.render(f"Hit", True, (255, 0, 0))
                                screen.fill("skyblue")
                                screen.blit(hit_text, (settings.GAMEWIDTH // 2 - hit_text.get_width() // 2, settings.GAMEHEIGHT // 2))
                                pygame.display.flip()
                                pygame.time.wait(500)
                            else:
                                miss_text = font.render(f"Miss", True, (0, 0, 255))
                                screen.fill("skyblue")
                                screen.blit(miss_text, (settings.GAMEWIDTH // 2 - miss_text.get_width() // 2, settings.GAMEHEIGHT // 2))
                                pygame.display.flip()
                                pygame.time.wait(500)
                            drawBoard(screen, currentPlayer, enemy)
                            if check_for_win(enemy):
                                font = pygame.font.Font(None, 48)
                                winner_text = font.render(f"Player {currentPlayer.num} Wins!", True, (255, 0, 0))
                                screen.fill("skyblue")
                                screen.blit(winner_text, (settings.GAMEWIDTH // 2 - winner_text.get_width() // 2, settings.GAMEHEIGHT // 2))
                                pygame.display.flip()
                                pygame.time.wait(3000)
                                return False, currentPlayer, enemy
                            waiting_for_input = False

    return True, currentPlayer, enemy


def check_for_win(player):
    return all(player.sunk_ships.get(ship_size, False) for ship_size in player.ships)


def showModeSelection(screen):
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
        screen.blit(ai_text, (ai_button_rect.centerx - ai_text.get_width() // 2, ai_button_rect.centery - ai_text.get_height() // 2))
        screen.blit(player_text, (player_button_rect.centerx - player_text.get_width() // 2, player_button_rect.centery - player_text.get_height() // 2))

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
