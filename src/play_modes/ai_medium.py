import logging

import pygame
import settings

from utils import *
from views import *
from models import Player, MediumAIGuessState


def _handle_medium_ai_turn(ai_opponent: Player, player, ai_guess_state: MediumAIGuessState):

    if ai_guess_state.tracking_player_ship(): #If first was a hit
        guessX, guessY = ai_guess_state.guess() #Get a guess from algorithm

        guess = None

        try:
            guess = ai_opponent.guesses[guessY][guessX] #Gets the passed guesses
        except IndexError:
            pass #if the next guess in algorithm is out of bounds Handles the excpetion

        if guess == 0:
            #Checks to see if the AI hit the other players ships
            hit = ai_opponent.check_hit(player, guessX, guessY)
            #if number of sunk ships increaes then reset AI to random guess
            if ai_guess_state.tracking_ship_sunk(player):
                ai_guess_state.stop_tracking_ship()
            elif hit:
                #If the next hit was a hit then continue with the guessing strategy
                ai_guess_state.track_player_ship((guessX, guessY))
            else:
                #if the hit was a miss then tally it as a bas gift
                ai_guess_state.next_guess()

            #Check if the player has won after the guess
            if check_for_win(player):
                handle_ai_win()
                return False
        else:
            #Mark a miss as a bad guess
            ai_guess_state.next_guess()
            #Calls function to handle medium ai difficulty
            return _handle_medium_ai_turn(ai_opponent, player, ai_guess_state)
        #returns true once the turn is complete
        return True
    else:
        #updates the amount of sunk ships
        ai_guess_state.curr_sunk_ships = player.count_sunk_ships()

        #Random positon for AI guess
        guessX = random.randint(0, 9)
        guessY = random.randint(0, 9)

        #Checks to see if the AI has guessed that position yet
        if ai_opponent.guesses[guessY][guessX] == 0:
            #Checks to see if the guess was a hit
            hit = ai_opponent.check_hit(player, guessX, guessY)

            if hit:
                #If it was a hit then start a roll
                ai_guess_state.track_player_ship((guessX, guessY))

            #Checks to see if player won after guess
            if check_for_win(player):
                handle_ai_win()
                return False
        else:
            #Handles the AI turn for medium
            return _handle_medium_ai_turn(ai_opponent, player, ai_guess_state)

        return True



def pvc_medium(count): #Ai medium
    clock = pygame.time.Clock()

    player: Player = Player(1)
    ai_opponent: Player = Player(2)

    random_placement(count, ai_opponent) #Places ships in the random spots for AI
    ai_guess_state = MediumAIGuessState() #Class that stores hits, sunk ships, and misses

    drawBackground() #Draws the blue background

    show_place_ships(count, player) #Lets you place ships for how many you have clicked


    game = True
    while game:
        drawBackground()

        game = show_active_game_view(player, ai_opponent, True) #Puts everything on the board and waits for input from Player
        game = _handle_medium_ai_turn(ai_opponent, player, ai_guess_state) #Waits for input from AiMedium mode

        clock.tick(settings.FPS)
