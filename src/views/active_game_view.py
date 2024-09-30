
import pygame


from utils import *


def show_active_game_view(currentPlayer: Player, enemy: Player, enemy_is_ai = False):
    """  # (N) function that handles the current player's turn.
        When a click event happens on the guess board, check for a hit or miss and update board accordingly.
        Some code taken from ChatGPT but mostly changed to fix errors
    """

    screen = getScreen()

    waiting_for_input = True  # (A) wait for input so the screen doesn't instantly move
    x_offset = 150  # (N) setting virtical and horizontal offset to specify the guess board on top
    y_offset = 30

     # Define the Exit button for the top-right positioning
    button_width = 100
    button_height = 40
    margin = 30
    exit_button_rect = pygame.Rect((settings.GAMEWIDTH - button_width - margin, margin), (button_width, button_height))
    exit_font = pygame.font.Font(None, 24)
    exit_text = exit_font.render("Exit Game", True, (255, 255, 255))

    while waiting_for_input:  # (A) input waiting loop
        # (A) draw the board based on player/enemy data (top is guesses, bottom is player)
        drawBoard(enemy.guesses, currentPlayer.board, currentPlayer.guesses)

 # Draw the exit button at the top right
        pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, 2)
        pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
        screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2,
                               exit_button_rect.centery - exit_text.get_height() // 2))

        pygame.display.flip()  # (A) update the screen with the rendered boards, and then wait for player to make a decision

        for event in pygame.event.get():  # (N) checking for events
            if event.type == pygame.QUIT:  # (N) if it is a quit event, return False meaning the game will end
                return False, None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:  # (N) if a click occurs
                if event.button == 1:
                    mouse_pos = event.pos
                    if exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    mouseX, mouseY = pygame.mouse.get_pos()  # (N) get the position of the mouse

                    # (N) looking for the specific position on the actual board
                    gridX = (mouseX - x_offset) // settings.BLOCKWIDTH
                    gridY = (mouseY - y_offset) // settings.BLOCKHEIGHT

                    if 0 <= gridX < settings.COLS and 0 <= gridY < settings.ROWS:  # (N) making sure the click is occuring on the guess board or it will not be inputted
                        if currentPlayer.guesses[gridY][gridX] == 0:  # (N) if the square hasn't been shot before
                            # (N) check if it was a hit or miss using the check_hit function
                            player_hit_ship = currentPlayer.check_hit(enemy, gridX, gridY)

                            # (N) check for a win by calling the function on the enemy, if that is the case and the current player has won
                            if check_for_win(enemy):
                                display_fullscreen_message('You WIN!!!', {
                                    'font-size': getFontSizePx('lg'),
                                    'color': getPygameColor('ship-hit')

                                })
                                pygame.time.wait(3_000)  # (N) wait a bit
                                return False

                            if player_hit_ship:
                                playSound('explosion')
                                msg = 'HIT! Please turn the screen to the next player' \
                                    if not enemy_is_ai else 'HIT! AI is now playing...'
                                display_fullscreen_message(msg, {
                                    'color': getPygameColor('ship-hit')
                                })
                            else:
                                playSound('missed')
                                msg = 'MISS! Please turn the screen to the next player' \
                                    if not enemy_is_ai else 'MISS! AI is now playing...'
                                display_fullscreen_message(msg, {
                                    'color': getPygameColor('ship-miss')
                                })
                            pygame.time.wait(settings.TURN_TIME_OUT_SECONDS * 1000)

                            # (N) redraw the board to show a hit or miss on the screen
                            drawBoard(enemy.guesses, currentPlayer.board, currentPlayer.guesses)


                            # (N) if the game isn't over just set waiting_for_input to be false so that the while loop ends
                            waiting_for_input = False

    return True

