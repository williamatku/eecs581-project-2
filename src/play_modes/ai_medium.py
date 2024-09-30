import logging

import pygame
import settings

from utils import *
from views import *
from models import Player, MediumAIGuessState


def ai_wins():
    display_fullscreen_message("The computer has prevailed, you lose", {
        'font-size': getFontSizePx('lg'),
        'color': getPygameColor('ship-hit')

    })
    pygame.time.wait(3_000)  # (N) wait a bit


def handleMediumAITurn(ai_opponent: Player, player, ai_guess_state: MediumAIGuessState):

    if ai_guess_state.on_a_roll: #If first was a hit
        mouseX, mouseY = ai_guess_state.produce_guess() #Get a guess from algorithm

        guess = None

        try:
            guess = ai_opponent.guesses[mouseY][mouseX] #Gets the passed guesses
        except IndexError:
            pass #if the next guess in algorithm is out of bounds Handles the excpetion

        if guess == 0:
            #Checks to see if the AI hit the other players ships
            hit = ai_opponent.check_hit(player, mouseX, mouseY)
            #if number of sunk ships increaes then reset AI to random guess
            if ai_guess_state.curr_sunk_ships < player.count_sunk_ships():
                ai_guess_state.reset()
            elif hit:
                #If the next hit was a hit then continue with the guessing strategy
                ai_guess_state.continue_roll((mouseX, mouseY))
            else:
                #if the hit was a miss then tally it as a bas gift
                ai_guess_state.bad_guess((mouseX, mouseY))

            #Check if the player has won after the guess
            if check_for_win(player):
                ai_wins()
                return False
        else:
            #Mark a miss as a bad guess
            ai_guess_state.bad_guess((mouseX, mouseY))
            #Calls function to handle medium ai difficulty
            return handleMediumAITurn(ai_opponent, player, ai_guess_state)
        #returns true once the turn is complete
        return True
    else:
        #updates the amount of sunk ships
        ai_guess_state.curr_sunk_ships = player.count_sunk_ships()

        #Random positon for AI guess
        mouseX = random.randint(0, 9)
        mouseY = random.randint(0, 9)

        #Checks to see if the AI has guessed that position yet
        if ai_opponent.guesses[mouseY][mouseX] == 0:
            #Checks to see if the guess was a hit
            hit = ai_opponent.check_hit(player, mouseX, mouseY)

            if hit:
                #If it was a hit then start a roll
                ai_guess_state.start_roll((mouseX, mouseY))

            #Checks to see if player won after guess
            if check_for_win(player):
                ai_wins()
                return False
        else:
            #Handles the AI turn for medium
            return handleMediumAITurn(ai_opponent, player, ai_guess_state)

        return True



def pvc_medium(count): #Ai medium
    clock = pygame.time.Clock()

    logging.info("You chose medium mode!")
    player = Player(1)
    ai_opponent: Player = Player(2)
    random_placement(count, ai_opponent) #Places ships in the random spots for AI
    ai_guess_state = MediumAIGuessState() #Class that stores hits, sunk ships, and misses

    drawBackground() #Draws the blue background


    showGameView(count, player) #Lets you place ships for how many you have clicked


    game = True
    while game:
        drawBackground()

        game = handlePlayerTurn(player, ai_opponent) #Puts everything on the board and waits for input from Player
        game = handleMediumAITurn(ai_opponent, player, ai_guess_state) #Waits for input from AiMedium mode

        clock.tick(settings.FPS)
