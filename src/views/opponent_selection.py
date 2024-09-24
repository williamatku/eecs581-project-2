
import pygame

import settings
from models import Player, PlayerTurn
from utils import drawLabels, createText, drawBackground


def showOpponentSelection(screen):
    # Text for the buttons
    ai_text = createText('med', "PVC", (255, 255, 255))  # White text for better contrast
    player_text = createText('med', "PVP", (255, 255, 255))

    # Button dimensions and positions
    button_width = 300
    button_height = 60
    ai_button_rect = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 200), (button_width, button_height))
    player_button_rect = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 300), (button_width, button_height))

    running = True
    while running:
        drawBackground(screen)

        # Add shadow effect for the buttons
        shadow_offset = 5
        pygame.draw.rect(screen, (0, 100, 0), ai_button_rect.move(shadow_offset, shadow_offset), border_radius=10)
        pygame.draw.rect(screen, (0, 100, 0), player_button_rect.move(shadow_offset, shadow_offset), border_radius=10)

        # Draw the buttons with rounded corners
        pygame.draw.rect(screen, (0, 200, 0), ai_button_rect, border_radius=10)  # Rounded corners with border_radius
        pygame.draw.rect(screen, (0, 200, 0), player_button_rect, border_radius=10)

        # Draw the text on the buttons
        screen.blit(ai_text, (
            ai_button_rect.centerx - ai_text.get_width() // 2,
            ai_button_rect.centery - ai_text.get_height() // 2
        ))
        screen.blit(player_text, (
            player_button_rect.centerx - player_text.get_width() // 2,
            player_button_rect.centery - player_text.get_height() // 2
        ))

        pygame.display.flip()  # Update screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # Check if clicked on AI button
                if ai_button_rect.collidepoint(mouse_pos):
                    print("AI mode selected")  # Placeholder until AI functionality is complete
                    running = False
                    return "AI"

                # Check if clicked on Play Against Player button
                if player_button_rect.collidepoint(mouse_pos):
                    print("Player mode selected")
                    running = False
                    return "Player"
