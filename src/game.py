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

from utils import handlePlayerTurn, drawBackground, getScreen, createText, getPygameColor, getFontSizePx, drawLabels, handleMiss, playSound
from views import showStartMenu, showGameView, showAIModeSelection, showTurnTransitionScreen, showOpponentSelection
from models import Player
from models import Player, PlayerTurn

def showTurnTransitionScreenAI(pturn: PlayerTurn):

    screen = getScreen()
    # Text for the buttons
    question_text = createText(f"Player {pturn}, are you ready?", {
        'font-size': getFontSizePx('med'),
        'color': getPygameColor('white')
    })  # White text for better contrast
    confirm_button_text = createText("Lets Battle", {
        'font-size': getFontSizePx('med'),
        'color': getPygameColor('white')
    })

    # Button dimensions and positions
    button_width = 300
    button_height = 60

    confirm_button = pygame.Rect((settings.GAMEWIDTH // 2 - button_width // 2, 300), (button_width, button_height))

    running = True
    while running:
        drawBackground()

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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Event listener when user clicks

                mouse_pos = event.pos # Get mouse location 
                if confirm_button.collidepoint(mouse_pos): # Confirm mouse over button
                    return "Confirmed" # Return confirmed which will tell pvc_hard to start gameplay loop

def drawBoardAIHard(player):  # Function that draws the player's board and the AI's guesses

    screen = getScreen()

    lineColor = (255, 255, 255)  # Color of the lines
    topOffset = 30  # Offset for the top board labels
    bottomOffset = 400  # Bottom offset to push the board down
    xOffset = 150  # Horizontal offset to center the boards

    # Draw the labels for the player's board
    drawLabels(screen, xOffset, topOffset)  
    for x in range(settings.COLS):  
        for y in range(settings.ROWS):  
            # Create a rectangle for the grid
            pyRect = (
                x * settings.BLOCKWIDTH + xOffset,
                y * settings.BLOCKHEIGHT + topOffset,
                settings.BLOCKWIDTH,
                settings.BLOCKHEIGHT
            )
            # Draw the grid lines
            pygame.draw.rect(screen, lineColor, pyRect, 1)

            # Display hits and misses on the player's own board
            if player.ai_misses[y][x] != 0:
                if player.ai_misses[y][x] == 'hit':  # If it's a hit
                    pygame.draw.rect(screen, (255, 0, 0), pyRect)  # Draw red for hits
                elif player.ai_misses[y][x] == 'miss':  # If it's a miss
                    pygame.draw.rect(screen, (0, 0, 255), pyRect)  # Draw blue for misses
                elif player.ai_misses[y][x] == 'sunk':  # If the ship is sunk
                    pygame.draw.rect(screen, (128, 128, 128), pyRect)  # Draw gray for sunk ships

    # Draw the AI's guess board at the bottom
    drawLabels(screen, xOffset, bottomOffset)
    
    for x in range(settings.COLS):  
        for y in range(settings.ROWS):
            # Create a rectangle for the AI's guess grid
            pyRect = (
                x * settings.BLOCKWIDTH + xOffset,
                y * settings.BLOCKHEIGHT + bottomOffset,
                settings.BLOCKWIDTH,
                settings.BLOCKHEIGHT
            )
            # Draw the grid lines
            pygame.draw.rect(screen, lineColor, pyRect, 1)

            # Display the player's ships on their own board
            if player.board[y][x] != 0:
                ship_size = player.board[y][x]  # Get the size of the ship
                ship_color = settings.SHIPCOLORS.get(ship_size, (0, 255, 0))  # Default to green if not found
                pygame.draw.rect(screen, ship_color, pyRect)  # Draw the ship

            # Show the AI's hits and misses on the player's ships
            if player.guesses[y][x] != 0:  # Check the player's guesses
                if player.guesses[y][x] == 'hit':
                    pygame.draw.rect(screen, getPygameColor('ship-hit'), pyRect)  # Hit - red
                elif player.guesses[y][x] == 'miss':
                    pygame.draw.rect(screen, getPygameColor('ship-miss'), pyRect)  # Miss - blue
                elif player.guesses[y][x] == 'sunk':
                    pygame.draw.rect(screen, getPygameColor('ship-sunk'), pyRect)  # Sunk - gray

def handleMissHardAI(): # Function used to handle a miss, which is every turn when on AI hard mode

    screen = getScreen()

    # almost same functionality as handleMiss(), but text displays that AI is making a move
    miss_text = createText(
        'MISS! Please wait while AI makes their move...',
        {
            'font-size': getFontSizePx('med'),
            'color': getPygameColor('ship-miss')
        }
    )

    drawBackground()
    playSound('missed')
    screen.blit(miss_text, (
        settings.GAMEWIDTH // 2 - miss_text.get_width() // 2,
        settings.GAMEHEIGHT // 2
    ))
    pygame.display.flip()

def playerTurnAIHard(player):
    waiting_for_input = True  # (A) wait for input so the screen doesn't instantly move
    x_offset = 150  # (N) setting virtical and horizontal offset to specify the guess board on top
    y_offset = 30
    while waiting_for_input:  # (A) input waiting loop
        # (A) draw the board based on player/enemy data (top is guesses, bottom is player)
        drawBoardAIHard(player)
        pygame.display.flip()  # (A) update the screen with the rendered boards, and then wait for player to make a decision

        for event in pygame.event.get():  # (N) checking for events
            if event.type == pygame.QUIT:  # (N) if it is a quit event, return False meaning the game will end
                return False, None, None
            elif event.type == pygame.MOUSEBUTTONDOWN:  # (N) if a click occurs
                if event.button == 1:

                    mouseX, mouseY = pygame.mouse.get_pos()  # (N) get the position of the mouse
                    # (N) looking for the specific position on the actual board
                    gridX = (mouseX - x_offset) // settings.BLOCKWIDTH
                    gridY = (mouseY - y_offset) // settings.BLOCKHEIGHT
                    if 0 <= gridX < settings.COLS and 0 <= gridY < settings.ROWS:  # (N) making sure the click is occuring on the guess board or it will not be inputted
                        player.ai_misses[gridY][gridX] = 'miss'
                        if player.guesses[gridY][gridX] == 0:  # (N) if the square hasn't been shot before
                            handleMissHardAI()
                            pygame.time.wait(settings.TURN_TIME_OUT_SECONDS * 1000)
                        waiting_for_input = False
                
    return False

def handleWinHardAI(): # Function called when hard AI wins a match

    screen = getScreen()

    # (N) display 'AI Wins!'
    winner_text = createText(
        f"AI Wins!",
        {
            'font-size': getFontSizePx('lg'),
            'color': (255, 0, 0)
        }
    )

    drawBackground()
    screen.blit(
        winner_text,
        (
            settings.GAMEWIDTH // 2 - winner_text.get_width() // 2,
            settings.GAMEHEIGHT // 2
        )
    )
    pygame.display.flip()
    pygame.time.wait(3000)  # (N) wait a bit
    return False # False is returned because this function is set to the variable game, so when game == False the application finishes running

def ai_hit(player, x, y):
    player.guesses[x][y] == 'hit' # This stores where the user has hit ships and saves it to guesses


def aiHardTurn(player, x, y):
    ai_hit(player, x, y)
    return True # Return True because the value of aiHardTurn is saved to users_turn, so user turn will start after this function
    

def pvc_hard(count): # Function to handle gameplay between user and AI hard mode
    screen = getScreen()
    clock = pygame.time.Clock()

    logging.info("You chose hard mode!")
    playerOne = Player(1)
    new_cheating_board = [] # Matrix to track where user put all of their ships (for cheating)

    drawBackground()

    game = True # Flag to show when game should still be happening or end
    setUp = True # Flag to show if user still needs to set up their ships on a board
    users_turn = False # Flag to show if user turn is happening or if AI is generating its move

    while game:
        drawBackground()
        
        if setUp:
            showGameView(count, playerOne) # Function for user to pick where they want to put their ships
            # AI gets matrix that says where all ships are
            cheating_board = playerOne.board # Temporary variable cheating board to put this information in new_cheating_board
            for list in cheating_board:
                new_cheating_board.append(list)
            logging.info(cheating_board)
            confirmed = showTurnTransitionScreenAI('1') # Variable to check if user has clicked confirm button
            setUp = False # Setup is complete so this flag is marked as False

            if confirmed == "Confirmed":
                users_turn = True  # Set the flag to true after confirmation

        else:  
            if users_turn: # user is doing a move
                turn_text = createText(f"Player 1's Turn", { # Display heading text
                    'font-size': getFontSizePx('sm'),
                    'color': getPygameColor('start-menu-text')
                })
                screen.blit(turn_text, (
                    settings.GAMEWIDTH // 2 - turn_text.get_width() // 2,
                    350
                ))
                users_turn = playerTurnAIHard(playerOne) # playerTurnAIHard will return False when the round is finished, so AI can make its move
            else:  # AI is doing a move
                # text to show user that AI is making a move on their board
                question_text = createText(f"AI making its move...", {
                    'font-size': getFontSizePx('med'),
                    'color': getPygameColor('white')
                })
                screen.blit(question_text, (
                    settings.GAMEWIDTH // 2 - question_text.get_width() // 2,
                    100
                ))

                move_made = False  # Flag to track if a move was made

                # iterate through the new_cheating_board matrix and keep track of indexes:
                y = -1
                for list in new_cheating_board:
                    y += 1
                    x = -1
                    for num in list:
                        x += 1
                        if num != 0:
                            new_cheating_board[y][x] = 0  # Change this cell to 0, indicating that it has been hit by the AI
                            playerOne.guesses[y][x] = 'hit'
                            move_made = True  # Set flag to indicate a move has been made
                            users_turn = aiHardTurn(playerOne, y, x)  # Process AI move
                            break  # Exit the inner loop
                    if move_made:  # If a move was made, break out of the outer loop as well
                        break
                
                if all(cell == 0 for row in new_cheating_board for cell in row):
                    print("player 1 looses!")
                    game = handleWinHardAI()

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        clock.tick(settings.FPS)

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

def start_game(): # (A) main function that starts the game
    pygame.init() # (A) initialize the pygame engine so it can listen for inputs/handle screens
    pygame.display.set_caption("battleship") # (A) set up the title of the game

    # initialize the main screen with a display of GAMEWIDTH and GAMEHEIGHT
    pygame.display.set_mode((settings.GAMEWIDTH, settings.GAMEHEIGHT))

    count = showStartMenu()  # (A) initial getCount() will be the default starting screen to find how many ships to play with

    # Call the mode selection screen
    mode = showOpponentSelection()


    if mode == "Player":  # If the user selected to play against another player
        pvp(count)

    elif mode == "AI":  # AI functionality placeholder

        difficulty = showAIModeSelection()

        if difficulty == "Easy":
            logging.error("AI mode is not implemented yet.")
            pass
        elif difficulty == "Medium":
            logging.error("AI mode is not implemented yet.")
            pass
        elif difficulty == "Hard":
            pvc_hard(count)
