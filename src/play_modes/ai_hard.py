import logging

import pygame
import settings
import sys

from utils import *
from views import showStartMenu, showGameView, showAIModeSelection, showTurnTransitionScreen, showOpponentSelection
from models import Player
from models import Player, PlayerTurn


def playerTurnAIHard(player: Player):
    waiting_for_input = True  # (A) wait for input so the screen doesn't instantly move
    x_offset = 150  # (N) setting virtical and horizontal offset to specify the guess board on top
    y_offset = 30
    while waiting_for_input:  # (A) input waiting loop
        # (A) draw the board based on player/enemy data (top is guesses, bottom is player)
        drawBoard(player.guesses, player.board, player.ai_misses)
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
                            display_fullscreen_message(
                                'MISS! Please wait while AI makes their move...',
                                {
                                    'font-size': getFontSizePx('med'),
                                    'color': getPygameColor('ship-miss')
                                }
                            )
                            playSound('missed')
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
