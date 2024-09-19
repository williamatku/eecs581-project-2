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

import sys
import pygame
import settings
from utils import getCount, startBoard, handlePlayerTurn, showModeSelection
from models import Player

def main():
    pygame.init()  # Initialize the pygame engine
    pygame.display.set_caption("Battleship")  # Set the window title
    
    screen = pygame.display.set_mode((settings.GAMEWIDTH, settings.GAMEHEIGHT))  # Create the game window
    clock = pygame.time.Clock()  # Create a clock to control the game's frame rate
    
    # Call the mode selection screen
    mode = showModeSelection(screen)
    
    if mode == "Player":  # If the user selected to play against another player
        count = getCount(screen)  # Get the number of ships for the game
        setUp = True  # Flag to indicate setup phase
        
        # Initialize players
        playerOne = Player(1)
        playerTwo = Player(2)
        currentPlayer = playerOne
        enemy = playerTwo
        
        game = True  # Main game loop flag
        while game:
            screen.fill("skyblue")  # Fill the screen background
            
            if setUp:  # Setup phase to place ships
                startBoard(screen, count, playerOne)
                startBoard(screen, count, playerTwo)
                setUp = False
            else:  # Main game phase
                font = pygame.font.Font(None, 28)
                turn_text = font.render(f"Player {currentPlayer.num}'s Turn", True, (5, 5, 5))
                screen.blit(turn_text, (settings.GAMEWIDTH // 2 - turn_text.get_width() // 2, 350))
                
                game, currentPlayer, enemy = handlePlayerTurn(screen, currentPlayer, enemy)  # Handle player turns
                if game:
                    currentPlayer, enemy = enemy, currentPlayer  # Swap players after each turn
            
            pygame.display.flip()  # Update the display
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handle the quit event
                    game = False
        
            clock.tick(settings.FPS)  # Control the frame rate
    
    elif mode == "AI":  # AI functionality placeholder
        print("AI mode is not implemented yet.")
        return  # Exit the game since AI mode is not yet available


if __name__ == "__main__":
    main()
