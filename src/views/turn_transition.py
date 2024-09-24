
import pygame

import settings
from models import Player, PlayerTurn
from utils import drawLabels, createText


def showTurnTransitionScreen(screen, pturn: PlayerTurn):

    # Text for the buttons
    question_text = createText('med', f"Player {pturn}, are you ready?", (255, 255, 255))  # White text for better contrast
    confirm_button_text = createText('med', "Lets Battle", (255, 255, 255))

    # Button dimensions and positions
    button_width = 300
    button_height = 60

    confirm_button = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 300), (button_width, button_height))

    running = True
    while running:
        screen.fill("skyblue")  # Clear screen with sky blue background

        # Add shadow effect for the buttons
        shadow_offset = 5
        pygame.draw.rect(screen, (0, 100, 0), confirm_button.move(shadow_offset, shadow_offset), border_radius=10)

        # Draw the buttons with rounded corners
        pygame.draw.rect(screen, (0, 200, 0), confirm_button, border_radius=10)

        # Draw the text on the buttons
        screen.blit(question_text, (
            settings.GAMEWIDTH // 2 - question_text.get_width() // 2,
            100
        ))
        screen.blit(confirm_button_text, (
            confirm_button.centerx - question_text.get_width() // 2,
            confirm_button.centery - question_text.get_height() // 2
        ))

        pygame.display.flip()  # Update screen

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                mouse_pos = event.pos
                # Check if clicked on AI button
                if confirm_button.collidepoint(mouse_pos):
                    print("Clicked")
                    return
