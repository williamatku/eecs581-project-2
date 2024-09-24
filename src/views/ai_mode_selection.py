import pygame
import settings
from utils import createText, drawBackground, getScreen, getFontSizePx, getPygameColor


def showAIModeSelection():

    screen = getScreen()

    # Text for the buttons
    easy_text = createText("AI Easy Mode", {
        'font-size': getFontSizePx('med'),
        'color': getPygameColor('white')
    })  # White text for better contrast
    medium_text = createText("AI Medium Mode",{
        'font-size': getFontSizePx('med'),
        'color': getPygameColor('white')
    })
    hard_text = createText("AI Hard Mode", {
        'font-size': getFontSizePx('med'),
        'color': getPygameColor('white')
    })

    # Button dimensions and positions
    button_width = 300
    button_height = 60
    easy_button_rect = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 200), (button_width, button_height))
    medium_button_rect = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 300), (button_width, button_height))
    hard_button_rect = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 400), (button_width, button_height))

    running = True
    while running:
        drawBackground()

        # Add shadow effect for the buttons
        shadow_offset = 5
        pygame.draw.rect(screen, (0, 100, 0), easy_button_rect.move(shadow_offset, shadow_offset), border_radius=10)
        pygame.draw.rect(screen, (0, 100, 0), medium_button_rect.move(shadow_offset, shadow_offset), border_radius=10)
        pygame.draw.rect(screen, (0, 100, 0), hard_button_rect.move(shadow_offset, shadow_offset), border_radius=10)

        # Draw the buttons with rounded corners
        pygame.draw.rect(screen, (0, 200, 0), easy_button_rect, border_radius=10)  # Rounded corners with border_radius
        pygame.draw.rect(screen, (0, 200, 0), medium_button_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 200, 0), hard_button_rect, border_radius=10)

        # Draw the text on the buttons
        screen.blit(easy_text, ( easy_button_rect.centerx - easy_text.get_width() // 2, easy_button_rect.centery - easy_text.get_height() // 2))
        screen.blit(medium_text, (medium_button_rect.centerx - medium_text.get_width() // 2, medium_button_rect.centery - medium_text.get_height() // 2))
        screen.blit(hard_text, ( hard_button_rect.centerx - hard_text.get_width() // 2, hard_button_rect.centery - hard_text.get_height() // 2))

        pygame.display.flip()  # Update screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # Check if clicked on AI button
                if easy_button_rect.collidepoint(mouse_pos):
                    print("easy mode selected")  # Placeholder until AI functionality is complete
                    running = False
                    return "Easy"

                # Check if clicked on Play Against Player button
                if medium_button_rect.collidepoint(mouse_pos):
                    print("medium mode selected")
                    running = False
                    return "Medium"

                if hard_button_rect.collidepoint(mouse_pos):
                    print("hard mode selected")  # Placeholder until AI functionality is complete
                    running = False
                    return "Hard"
