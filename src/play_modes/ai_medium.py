import logging

import pygame
import settings
import sys

from utils import *
from views import showStartMenu, showGameView, showAIModeSelection, showTurnTransitionScreen, showOpponentSelection
from models import Player, AIGuessState


def pvc_medium(count): #Ai medium
    clock = pygame.time.Clock()

    logging.info("You chose medium mode!")
    player = Player(1)
    ai_opponent: Player = Player(2)
    random_placement(count, ai_opponent) #Places ships in the random spots for AI
    ai_guess_state = AIGuessState() #Class that stores hits, sunk ships, and misses

    drawBackground() #Draws the blue background


    showGameView(count, player) #Lets you place ships for how many you have clicked


    game = True
    while game:
        drawBackground()

        logging.info('player turn init')
        game = handlePlayerTurn(player, ai_opponent) #Puts everything on the board and waits for input from Player
        logging.info('ai turn init')
        game = handleMediumAITurn(ai_opponent, player, ai_guess_state) #Waits for input from AiMedium mode

        clock.tick(settings.FPS)
