import logging

import pygame
import settings
import sys

from utils import *
from views import showStartMenu, showGameView, showAIModeSelection, showTurnTransitionScreen, showOpponentSelection
from models import Player
from models import Player, PlayerTurn


def drawBoardAIHard(player):  # Function that draws the player's board and the AI's guesses

    screen = getScreen()

    lineColor = (255, 255, 255)  # Color of the lines
    topOffset = 30  # Offset for the top board labels
    bottomOffset = 400  # Bottom offset to push the board down
    xOffset = 150  # Horizontal offset to center the boards

    # Draw the labels for the player's board
    drawLabels(xOffset, topOffset)
    for x in range(settings.COLS):
        for y in range(settings.ROWS):
            # Create a rectangle for the grid
            pyRect = (
                x * settings.BLOCKWIDTH + xOffset,
                y * settings.BLOCKHEIGHT + topOffset,
                settings.BLOCKWIDTH,
                settings.BLOCKHEIGHT
            )
            # Draw the grid lines
            pygame.draw.rect(screen, lineColor, pyRect, 1)

            # Display hits and misses on the player's own board
            if player.ai_misses[y][x] != 0:
                if player.ai_misses[y][x] == 'hit':  # If it's a hit
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)  # Draw red for hits
                elif player.ai_misses[y][x] == 'miss':  # If it's a miss
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)  # Draw blue for misses
                elif player.ai_misses[y][x] == 'sunk':  # If the ship is sunk
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)  # Draw gray for sunk ships

    # Draw the AI's guess board at the bottom
    drawLabels(xOffset, bottomOffset)

    for x in range(settings.COLS):
        for y in range(settings.ROWS):
            # Create a rectangle for the AI's guess grid
            pyRect = (
                x * settings.BLOCKWIDTH + xOffset,
                y * settings.BLOCKHEIGHT + bottomOffset,
                settings.BLOCKWIDTH,
                settings.BLOCKHEIGHT
            )
            # Draw the grid lines
            pygame.draw.rect(screen, lineColor, pyRect, 1)

            # Display the player's ships on their own board
            if player.board[y][x] != 0:
                ship_size = player.board[y][x]  # Get the size of the ship
                ship_image = settings.SHIPIMAGE.get(ship_size)  # (M) get the type of color from matching it to the global colors
                ship_image = pygame.transform.scale(ship_image, (
                settings.BLOCKHEIGHT, settings.BLOCKWIDTH))  # transforms the ship image to fit inside the square
                pygame.Surface.blit(screen, ship_image, pyRect)  # Displays ship image to screen where player choses.

            # Show the AI's hits and misses on the player's ships
            if player.guesses[y][x] != 0:  # Check the player's guesses
                if player.guesses[y][x] == 'hit':
                    pygame.draw.rect(screen, getPygameColor('ship-hit'), pyRect)  # Hit - red
                elif player.guesses[y][x] == 'miss':
                    pygame.draw.rect(screen, getPygameColor('ship-miss'), pyRect)  # Miss - blue
                elif player.guesses[y][x] == 'sunk':
                    pygame.draw.rect(screen, getPygameColor('ship-sunk'), pyRect)  # Sunk - gray


def handleMissHardAI():  # Function used to handle a miss, which is every turn when on AI hard mode

    screen = getScreen()

    # almost same functionality as handleMiss(), but text displays that AI is making a move
    miss_text = createText(
        'MISS! Please wait while AI makes their move...',
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


def playerTurnAIHard(player):
    waiting_for_input = True  # (A) wait for input so the screen doesn't instantly move
    x_offset = 150  # (N) setting virtical and horizontal offset to specify the guess board on top
    y_offset = 30
    while waiting_for_input:  # (A) input waiting loop
        # (A) draw the board based on player/enemy data (top is guesses, bottom is player)
        drawBoardAIHard(player)
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
                        player.ai_misses[gridY][gridX] = 'miss'
                        if player.guesses[gridY][gridX] == 0:  # (N) if the square hasn't been shot before
                            handleMissHardAI()
                            pygame.time.wait(settings.TURN_TIME_OUT_SECONDS * 1000)
                        waiting_for_input = False

    return False


def handleWinHardAI():  # Function called when hard AI wins a match

    screen = getScreen()

    # (N) display 'AI Wins!'
    winner_text = createText(
        "AI Wins!",
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
    return False  # False is returned because this function is set to the variable game, so when game == False the application finishes running


def pvc_hard(count):  # Function to handle gameplay between user and AI hard mode
    screen = getScreen()
    clock = pygame.time.Clock()

    logging.info("You chose hard mode!")
    playerOne = Player(1)
    new_cheating_board = []  # Matrix to track where user put all of their ships (for cheating)

    drawBackground()

    game = True  # Flag to show when game should still be happening or end
    setUp = True  # Flag to show if user still needs to set up their ships on a board
    users_turn = False  # Flag to show if user turn is happening or if AI is generating its move

    while game:
        drawBackground()

        if setUp:
            showGameView(count, playerOne)  # Function for user to pick where they want to put their ships
            # AI gets matrix that says where all ships are
            cheating_board = playerOne.board  # Temporary variable cheating board to put this information in new_cheating_board
            for list in cheating_board:
                new_cheating_board.append(list)

            showTurnTransitionScreen(1)  # Variable to check if user has clicked confirm button
            setUp = False  # Setup is complete so this flag is marked as False
            users_turn = True  # Set the flag to true after confirmation

        else:
            if users_turn:  # user is doing a move
                turn_text = createText("Your Turn", {  # Display heading text
                    'font-size': getFontSizePx('sm'),
                    'color': getPygameColor('start-menu-text')
                })
                screen.blit(turn_text, (
                    settings.GAMEWIDTH // 2 - turn_text.get_width() // 2,
                    350
                ))
                users_turn = playerTurnAIHard(
                    playerOne)  # playerTurnAIHard will return False when the round is finished, so AI can make its move
            else:  # AI is doing a move
                # text to show user that AI is making a move on their board
                question_text = createText("AI making its move...", {
                    'font-size': getFontSizePx('med'),
                    'color': getPygameColor('white')
                })
                screen.blit(question_text, (
                    settings.GAMEWIDTH // 2 - question_text.get_width() // 2,
                    100
                ))

                move_made = False  # Flag to track if a move was made

                # iterate through the new_cheating_board matrix and keep track of indexes:
                y = -1
                for list in new_cheating_board:
                    y += 1
                    x = -1
                    for num in list:
                        x += 1
                        if num != 0:
                            # Change this cell to 0, indicating that it has been hit by the AI
                            new_cheating_board[y][x] = 0
                            playerOne.guesses[y][x] = 'hit'
                            move_made = True  # Set flag to indicate a move has been made

                            # This stores where the user has hit ships and saves it to guesses
                            playerOne.guesses[x][y] == 'hit'
                            users_turn = True  # user turn will start after this function
                            break  # Exit the inner loop
                    if move_made:  # If a move was made, break out of the outer loop as well
                        break

                if all(cell == 0 for row in new_cheating_board for cell in row):
                    print("player 1 looses!")
                    game = handleWinHardAI()

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        clock.tick(settings.FPS)
