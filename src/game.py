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
import sys

from utils import *
from views import showStartMenu, showGameView, showAIModeSelection, showTurnTransitionScreen, showOpponentSelection
from models import Player, AIGuessState


def pvp(ship_count):

    screen = getScreen()
    clock = pygame.time.Clock() # (A) clock that keeps track of how many times the screen is updated

    playerOne = Player(1)  # (A) initialize playerOne, with a Player(num)-- num marker of 1 to differentiate
    playerTwo = Player(2)  # (A) playertwo with player.num = 2

    currentPlayer = playerOne  # (A) game will start with playerOne, so currentPlayer is initialized
    enemy = playerTwo  # (A) enemy for now is playerTwo, but these roles will be swapped every game loop

    game = True  # (A) game conditional loop
    setUp = True  # (A) check that'll only run the startBoard() once for ships

    while game:  # (A) while the game is running
        drawBackground()
        if setUp:  # (A) conditional met with first time run of the loop
            showGameView(ship_count, playerOne)  # (A) create the matrix for playerOne with ship selection
            showTurnTransitionScreen('2')
            showGameView(ship_count, playerTwo)  # (A) do the same for playerTwo
            showTurnTransitionScreen('1')
            setUp = False  # (A) set condition to false, won't run again for remainder of the game
        else:  # (A) when the boards have been set up
            turn_text = createText(f"Player {currentPlayer.num}'s Turn", {
                'font-size': getFontSizePx('sm'),
                'color': getPygameColor('start-menu-text')
            })  # (A) render the text
            screen.blit(turn_text, (
                settings.GAMEWIDTH // 2 - turn_text.get_width() // 2,
                350
            ))  # (A) push the rendered text to the top of the screen, placed horizontal and in the middle vertically

            # (A) handle the player turn, will swap players (curr/enemy) after each successful playerturn
            game, currentPlayer, enemy = handlePlayerTurn(currentPlayer, enemy)
            if game:  # (A) if the game is still going on... may be a redundant conditional in hindsight
                showTurnTransitionScreen(currentPlayer.num)
                currentPlayer, enemy = enemy, currentPlayer  # (A) then swap the two players

        pygame.display.flip()  # (A) flip to update the display as needed
        for event in pygame.event.get():  # (A) listen to events
            if event.type == pygame.QUIT:  # (A) if user exits out
                game = False  # (A) game is over
        clock.tick(settings.FPS)  # (A) FPS (initialized at the start of the code) will determine refresh rate for the game


def pvc_hard(count):

    screen = getScreen()
    clock = pygame.time.Clock() # (A) clock that keeps track of how many times the screen is updated

    logging.info("You chose hard mode!")
    playerOne = Player(1)  # (A) initialize playerOne, with a Player(num)-- num marker of 1 to differentiate
    drawBackground()

    # player picks their ships using startBoard
    showGameView(count, playerOne)  # (A) create the matrix for playerOne (only player)

    # AI gets matrix that says where all ships are
    cheating_board = playerOne.board
    logging.info(cheating_board)

    game = True  # (A) game conditional loop
    setUp = True  # (A) check that'll only run the startBoard() once for ships

    while game:
        drawBackground()
        font = pygame.font.Font(None, 28)  # (A) font object with no font type and 28 font size
        turn_text = createText(f"Player {playerOne.num}'s Turn", {
            'color': (5, 5, 5),
            'font-size': getFontSizePx('med'),
        })  # (A) render the text

        # (A) push the rendered text to the top of the screen, placed horizontal and in the middle vertically
        screen.blit(turn_text, (settings.GAMEWIDTH // 2 - turn_text.get_width() // 2, 350))
        # (A) handle the player turn, will swap players (curr/enemy) after each successful playerturn
        game, currentPlayer, enemy = handlePlayerTurn(currentPlayer, enemy)
        if game:  # (A) if the game is still going on... may be a redundant conditional in hindsight
            currentPlayer, enemy = enemy, currentPlayer  # (A) then swap the two players

    pygame.display.flip()  # (A) flip to update the display as needed
    for event in pygame.event.get():  # (A) listen to events
        if event.type == pygame.QUIT:  # (A) if user exits out
            game = False  # (A) game is over

    clock.tick(settings.FPS)  # (A) FPS (initialized at the start of the code) will determine refresh rate for the game



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
        ai_opponent.spit_guesses() #Shows your guesses 

        clock.tick(settings.FPS)  


def start_game():
    pygame.init() 
    pygame.display.set_caption("battleship") 

    # initialize the main screen with a display of GAMEWIDTH and GAMEHEIGHT
    pygame.display.set_mode((settings.GAMEWIDTH, settings.GAMEHEIGHT))

    count = showStartMenu() 
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
