import settings
import logging

from typing import Optional

type PlayerTurn = '1' | '2'


class Player:  # stores the data for each player so we can alternate easily with each turn based on the Player data
    def __init__(self, num):  # (A) initialization
        self.num = num  # (A) player num to keep track of who's who without anything fancy
        self.board = [[0 for _ in range(settings.COLS)] for _ in
                      range(settings.ROWS)]  # (A) initialize player's matrix based on game board to reflect ship states
        self.guesses = [[0 for _ in range(settings.COLS)] for _ in
                        range(settings.ROWS)]  # (A) similarly, a matrix to reflect guesses on the enemy that are accurate/misses
        self.ships = {}  # (N) a dict for the ships that will hold the size of the ships and the number of times the ship has been hit
        self.sunk_ships = {}  # (N) dict that holds the ships that are sunk that belong to the player themselves

    def place_ship(self, x, y, size, direction):  # (A) return if valid placement based on player's board
        if direction == 0:  # (A) refers to the current direction being used in the start screen that was passed through (0 is to the right)
            if x + size > settings.COLS:  # (A) too large for the board
                return False  # (A) not a valid move
            for i in range(
                    size):  # (A) now if not too large, we must calculate if there are any collisions with other placements
                if self.board[y][x + i] != 0:  # (A) if not 0 so not free in the path of placement...
                    return False  # (A) then this is not a valid move
            for i in range(size):  # (A) otherwise, replace the path with ships of size
                self.board[y][
                    x + i] = size  # (A) important to set nodes in the path to 'size' because that will distinguish different ships
        elif direction == 1:  # (A) similarly, refer to the above; direction == 1 means it is a path pointing down
            if y + size > settings.ROWS:
                return False
            for i in range(size):
                if self.board[y + i][x] != 0:
                    return False
            for i in range(size):
                self.board[y + i][x] = size
        elif direction == 2:  # (A) refer to above, direction == 2 means it is a path pointing to the left
            if x - size + 1 < 0:  # (A) distinction between this conditinoal and the above is that 0 can be valid, but ROWS/COLS cannot hence the + 1
                return False
            for i in range(size):
                if self.board[y][x - i] != 0:
                    return False
            for i in range(size):
                self.board[y][x - i] = size
        elif direction == 3:  # (A) refer to above, direction == 3 means it is a path pointing to the top
            if y - size + 1 < 0:  # (A) same explanation as direction == 2 for this conditional
                return False
            for i in range(size):
                if self.board[y - i][x] != 0:
                    return False
            for i in range(size):
                self.board[y - i][x] = size

        if size not in self.ships:  # (N) initializing the dicts for the self.ships and self.sunk_ships for each ship size on the board. They are initialized to 0 and False respectively. Adapted from ChatGPT but changed to fit the logic and fix some errors
            self.ships[size] = 0
            self.sunk_ships[size] = False
        return True

    def check_hit(self, enemy, x,
                  y):  # (N) function that checks for a hit on an enemy ship. Takes in the parameters the enemy player object as well as the x and y coordinates on the board that was fired at. Partially taken from ChatGPT but mostly changed to fix issues with the function
        if enemy.board[y][x] > 0:  # (N) checking to see if the size of a ship is marked on that space of the board
            ship_size = enemy.board[y][x]  # (N) if that is the case assign a variable to be the size of that ship
            self.guesses[y][x] = 'hit'  # (N) add to the player guesses that the coordinate was a hit
            enemy.ships[ship_size] += 1  # (N) add a hit count to the specific ship of the size that was hit
            if enemy.ships[ship_size] == ship_size and not enemy.sunk_ships[
                ship_size]:  # (N) if the # of hits are the same as the size of the ship, and it is not already sunk
                enemy.mark_ship_as_sunk(self,
                                        ship_size)  # (N) mark the ship as sunk in the enemy's dict of sunk ships (meaning that the enemy keeps track of which of their ships are sunk not the current player)
            return True  # (N) return that the shot was a hit
        else:
            self.guesses[y][x] = 'miss'  # (N) or the shot is a miss and return that it is a miss
            return False

    def mark_ship_as_sunk(self, currentPlayer,
                          ship_size):  # (N) function that will mark a ship as sunk in the enemy's dict of their own ships. Initially adapted from ChatGPT but almost fully changed to fit the program logic
        self.sunk_ships[
            ship_size] = True  # (N) mark in your own dict of sunken ships (in this case the enemy) that the ship of that size is sunk
        for y in range(settings.ROWS):  # (N) iterate through all cols and rows
            for x in range(settings.COLS):
                if self.board[y][
                    x] == ship_size:  # (N) if any spaces correspond to the size of the ship that was sunk, mark them as sunk in the player's guesses, not the enemy's
                    currentPlayer.guesses[y][x] = 'sunk'

    def count_sunk_ships(self):

        logging.info(self.sunk_ships)

        #Checks to see if the ships are sunk 
        s1 = 1 if self.sunk_ships.get(1) else 0
        s2 = 1 if self.sunk_ships.get(2) else 0
        s3 = 1 if self.sunk_ships.get(3) else 0
        s4 = 1 if self.sunk_ships.get(4) else 0
        s5 = 1 if self.sunk_ships.get(5) else 0

        #Returns all the sunk ships 
        return s1 + s2 + s3 + s4 + s5

    def spit_board(self):
        for row in self.board:
            print(row)

    def spit_guesses(self):
        for row in self.guesses:
            print(row)
        print()


class AIGuessState:
    def __init__(self):
        self.on_a_roll = False #Checks if the AI is currently on a ROLL
        self.first_successful_guess: Optional[(int, int)] = None #Stores the first hit in a tuple
        self.last_successful_guess: Optional[(int, int)] = None #Stores the last hit in a tuple
        self.curr_sunk_ships = None #Current number of sunk ships
        self.guesses = [] #stores all the guesses made in a list
        self.orientation = 0 #If two correct guesses in a row then change orientation to go the same direction 
        self.failed_guesses = 0 #Counts all the failed guesses 

    def start_roll(self, fsg): #Starts a roll with the first correct guess
        self.on_a_roll = True
        self.first_successful_guess = fsg
        self.last_successful_guess = fsg
        self.guesses.append(fsg) #adds guess to the list

    def continue_roll(self, lsg): #Continutes the roll with the last correct guess
        self.last_successful_guess = lsg
        self.failed_guesses = 0
        self.guesses.append(lsg) #adds guess to the list 

    def bad_guess(self, bad_guezz):
        logging.info(f'bad guess {self.failed_guesses}')

        self.guesses.append(bad_guezz)
        if self.failed_guesses > 3:
            #Resets to first correct guess if more than 3 consecutive guesses
            self.last_successful_guess = self.first_successful_guess
            self.failed_guesses = 0
        else:
            #Changes the orientation and increments failed guesses
            self.orientation = (self.orientation + 1) % 4
            self.failed_guesses += 1

    def produce_guess(self):
        last_was_success = self.last_successful_guess != None
        x, y = None, None
        if last_was_success:
            x, y = self.last_successful_guess
        else:
            x, y = self.first_successful_guess

        #Generates the next guess based on this algorithm
        match self.orientation:
            case 0:
                return x, y + 1
            case 1:
                return x + 1, y
            case 2:
                return x, abs(y - 1)
            case 3:
                return abs(x - 1), y

    def reset(self):
        #Resets to the initial values 
        self.orientation = 0
        self.last_successful_guess = None
        self.first_successful_guess = None
        self.guesses = []
        self.failed_guesses = 0
        self.on_a_roll = False
        self.curr_sunk_ships = None
