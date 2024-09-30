# ai_easy.py
import logging
import pygame
import random
import settings

from utils import *
from views import *
from models import Player, PlayerTurn


def handleEasyAITurn(ai_opponent: Player, player: Player):
    # Random position for AI guess
    guessX = random.randint(0, 9)
    guessY = random.randint(0, 9)

    # Checks to see if the AI has guessed that position yet
    if ai_opponent.guesses[guessY][guessX] == 0:
        # Checks to see if the guess was a hit
        hit = ai_opponent.check_hit(player, guessX, guessY)

        # Check if the ai has won after the guess
        if check_for_win(player):
            handle_ai_win()
            return False

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
    show_place_ships(count, player)  # Lets you place ships for the selected count

    game = True
    while game:
        drawBackground()

        game = show_active_game_view(player, ai_opponent)  # Player's turn to play
        game = handleEasyAITurn(ai_opponent, player)  # AI's turn to make a random guess

        clock.tick(settings.FPS)