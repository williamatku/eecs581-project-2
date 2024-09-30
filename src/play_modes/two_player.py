import logging

import pygame
import settings
import sys

from utils import *
from views import showStartMenu, show_place_ships, showAIModeSelection, show_turn_transition, showOpponentSelection, show_active_game_view
from models import Player
from models import Player, PlayerTurn


def pvp(ship_count):

    screen = getScreen()
    clock = pygame.time.Clock() # (A) clock that keeps track of how many times the screen is updated

    playerOne = Player(1)  # (A) initialize playerOne, with a Player(num)-- num marker of 1 to differentiate
    playerTwo = Player(2)  # (A) playertwo with player.num = 2

    currentPlayer = playerOne  # (A) game will start with playerOne, so currentPlayer is initialized
    enemy = playerTwo  # (A) enemy for now is playerTwo, but these roles will be swapped every game loop

    game = True  # (A) game conditional loop
    setUp = True  # (A) check that'll only run the startBoard() once for ships

    button_width = 100
    button_height = 40
    margin = 30  # Margin from the top and right edges
    exit_button_rect = pygame.Rect((settings.GAMEWIDTH - button_width - margin, margin), (button_width, button_height))
    exit_font = pygame.font.Font(None, 24)
    exit_text = exit_font.render("Exit Game", True, (255, 255, 255))

    while game:  # (A) while the game is running
        drawBackground()
        if setUp:  # (A) conditional met with first time run of the loop
            show_place_ships(ship_count, playerOne)  # (A) create the matrix for playerOne with ship selection
            show_turn_transition('2')
            show_place_ships(ship_count, playerTwo)  # (A) do the same for playerTwo
            show_turn_transition('1')
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
            game = show_active_game_view(currentPlayer, enemy)
            if game:  # (A) if the game is still going on... may be a redundant conditional in hindsight
                currentPlayer, enemy = enemy, currentPlayer  # (A) then swap the two players
                show_turn_transition(currentPlayer.num)

            # Draw the exit button on the gameplay screen
            pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, 2)  # Draw a black border for visibility
            pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)  # Draw the red button
            screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2,
                                    exit_button_rect.centery - exit_text.get_height() // 2))

        pygame.display.flip()  # (A) flip to update the display as needed


        for event in pygame.event.get():  # (A) listen to events
            if event.type == pygame.QUIT:  # (A) if user exits out
                game = False  # (A) game is over
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button click
                        mouse_pos = event.pos
                        print(f"Mouse click at: {mouse_pos}")
                        if exit_button_rect.collidepoint(mouse_pos):
                            print("Exit button clicked")
                            pygame.quit()
                            sys.exit()

        clock.tick(settings.FPS)  # (A) FPS (initialized at the start of the code) will determine refresh rate for the game
