"""
Name: Battleship
Description: An implementation of battleship that follows the guidelines outlined in the rubric.
Players will determine how many ships at the start, and will guess ships on the enemy's board, switching after each guess.
Inputs: Number of battleships, Rotation/Alignment of ship placement, Where to hit a ship
Output: A functional battleship game that ends after all ships of one side has been sunk. 
Other Sources: ChatGPT
Author(s): Anil Thapa, Michelle Chen, Nathan Bui
Creation Date: 09/13/2024
"""
import logging

import pygame
import settings

from views import showStartMenu, showOpponentSelection, showAIModeSelection
from play_modes import *

def start_game(): # (A) main function that starts the game
    pygame.init() # (A) initialize the pygame engine so it can listen for inputs/handle screens
    pygame.display.set_caption("battleship") # (A) set up the title of the game

    # initialize the main screen with a display of GAMEWIDTH and GAMEHEIGHT
    pygame.display.set_mode((settings.GAMEWIDTH, settings.GAMEHEIGHT))

    while True:
        count = showStartMenu()  # (A) initial getCount() will be the default starting screen to find how many ships to play with

        # Call the mode selection screen
        mode = showOpponentSelection()
        if mode == "Player":  # If the user selected to play against another player
            pvp(count)

        elif mode == "AI":  # AI functionality placeholder

            difficulty = showAIModeSelection()

            if difficulty == "Easy":
                logging.error("AI mode is not implemented yet.")
                pass
            elif difficulty == "Medium":
                pvc_medium(count)
            elif difficulty == "Hard":
                pvc_hard(count)
        elif mode == "Go Back":
            start_game()
