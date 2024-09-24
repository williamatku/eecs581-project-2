
import pygame
import sys

import settings
from models import Player, PlayerTurn
from utils import drawLabels, createText, drawBackground, getRGBColor, getFontSizePx


def showStartMenu():  # (M) initial screen that determines how many ships the players will deal with

    screen = pygame.display.get_surface()

    title = createText("Battleship", {
        'font-size': getFontSizePx('lg'),
        'color': getRGBColor('start-menu-text')
    })
    prompt = createText("How many ships would you like? (1-5)", {
        'font-size': getFontSizePx('med'),
        'color': getRGBColor('start-menu-text')
    })
    startText = createText("Press ENTER to start", {
        'font-size': getFontSizePx('med'),
        'color': getRGBColor('start-menu-text')
    })
    disclaimer = createText("Use the up and down arrows to adjust the # of ships", {
        'font-size': getFontSizePx('sm'),
        'color': getRGBColor('start-menu-text')
    })

    ship_count = 1  # (M) minimum number of ships we can play with is one
    running = True  # (M) conditional for the game loop to continue

    while running:  # (M) this loop is necessary so the player can input their decisions without it going straight to the next screen
        drawBackground()

        screen.blit(title, (settings.GAMEWIDTH // 2 - title.get_width() // 2,
                            100))  # (M) place a rendered object on top of the screen, in this case our texts
        screen.blit(prompt, (settings.GAMEWIDTH // 2 - prompt.get_width() // 2,
                             200))  # (M) this will make the texts visible, and takes in x, y parameters
        screen.blit(startText, (settings.GAMEWIDTH // 2 - startText.get_width() // 2,
                                400))  # (M) GAMEWIDTH // 2 - text.get_width() // 2 helps center in the horizontal plane
        screen.blit(startText, (settings.GAMEWIDTH // 2 - startText.get_width() // 2,
                                400))  # (M) vertical placement is subjective, so we just pick whatever looks appealing
        screen.blit(disclaimer,
                    (settings.GAMEWIDTH // 2 - disclaimer.get_width() // 2, 450))  # (M) placing another text onto the screen

        # (M) new text to render inside the loop because it's dependent on the count of what the user has chosen
        count_text = createText(str(ship_count),{
            'font-size': getFontSizePx('med'),
            'color': getRGBColor('start-menu-text')
        })
        screen.blit(count_text, (
            settings.GAMEWIDTH // 2 - count_text.get_width() // 2,
            300
        ))  # (M) we will still need to place this to the top of the screen

        pygame.display.flip()  # (M) pygame.display.flip() will update the screen with the newly placed objects

        for event in pygame.event.get():  # (M) gameplay loop for listening to inputs within the game
            if event.type == pygame.QUIT:  # (M) if you close out, this is a pygame.QUIT event and ends the screen/game
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # (M) keydown refers to the act of pushing any key down, not just the down key
                if event.key == pygame.K_UP:  # (M) if this is going up, then user wants more ships
                    # (M) however, max count is 5, so if the user wants more than 5, just take the 5 which will be the min
                    ship_count = min(ship_count + 1, 5)
                elif event.key == pygame.K_DOWN:  # (M) likewise if this goes down, the user wants less ships
                    ship_count = max(ship_count - 1, 1)  # (M) but ship count is lower bound by 1
                elif event.key == pygame.K_RETURN:  # (M) if user presses enter, then we are good to send the ship count back
                    return ship_count  # (M) this allows for the shipcount to be sent back to main() and get used by game for selection and gameplay

    return ship_count  # (M) if the running is broken in any way, default is 1
