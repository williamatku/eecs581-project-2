# ai_easy.py
import logging
import pygame
import random
import settings

from utils import handlePlayerTurn, drawBackground, getScreen, createText, getPygameColor, getFontSizePx, check_for_win, handleWin
from views import showGameView
from models import Player
import logging
import random
import pygame
import settings
import sys

from utils import handlePlayerTurn, drawBackground, getScreen, createText, getPygameColor, getFontSizePx, drawLabels, \
    handleMiss, playSound
from views import showStartMenu, showGameView, showAIModeSelection, showTurnTransitionScreen, showOpponentSelection
from models import Player
from models import Player, PlayerTurn

def random_placement(count, player):
    """Randomly places ships on the board for the given player."""
    for ship_size in range(1, count + 1):
        placed = False
        while not placed:
            x = random.randint(0, settings.COLS - 1)
            y = random.randint(0, settings.ROWS - 1)
            direction = random.randint(0, 3)  # 0: right, 1: down, 2: left, 3: up
            placed = player.place_ship(x, y, ship_size, direction)

def handleEasyAITurn(ai_opponent: Player, player: Player):
    # Random position for AI guess
    mouseX = random.randint(0, 9)
    mouseY = random.randint(0, 9)

    # Checks to see if the AI has guessed that position yet
    if ai_opponent.guesses[mouseY][mouseX] == 0:
        # Checks to see if the guess was a hit
        hit = ai_opponent.check_hit(player, mouseX, mouseY)

        # Check if the player has won after the guess
        if check_for_win(player):
            return handleWin(ai_opponent, player)
    else:
        # Retry if the randomly selected cell was already guessed
        return handleEasyAITurn(ai_opponent, player)

    return True  # Return True to continue the game


def pvc_easy(count):
    screen = getScreen()
    clock = pygame.time.Clock()

    logging.info("You chose easy mode!")
    player = Player(1)
    ai_opponent = Player(2)
    random_placement(count, ai_opponent)  # Place ships randomly for AI

    drawBackground()  # Draw the blue background
    showGameView(count, player)  # Lets you place ships for the selected count

    game = True
    while game:
        drawBackground()

        logging.info('Player turn init')
        game = handlePlayerTurn(player, ai_opponent)  # Player's turn to play
        logging.info('AI turn init')
        
        if game:  # Only let the AI make a turn if the player hasn't won yet
            game = handleEasyAITurn(ai_opponent, player)  # AI's turn to make a random guess

        clock.tick(settings.FPS)