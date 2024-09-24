# Battleship Game EECS 581

A Python implementation of the classic battleship game using the pygame library. The game supports 1-2 players, allowing you to place ships on a grid and take turns guessing the positions of the opponent's ships.

## Features

- **User Interface:** Simple UI to select the number of ships, place them, and take turns.
- **Grid System:** 10x10 grid where ships can be placed horizontally or vertically.
- **Interactive Ship Placement:** Rotate ships and place them by clicking on the grid.
- **Turn-Based Gameplay:** Players take turns to guess the location of opponent ships.

## Screenshots

<img src="static/images/game_start.png" alt="Game Start" width="400">
<img src="static/images/player_1.png" alt="Player 1 Ship Placement" width="400">
<img src="static/images/player_2.png" alt="Player 2 Ship Placement" width="400">
<img src="static/images/gameplay.png" alt="Gameplay" width="400">
<img src="static/images/hit.png" alt="Hit Screen" width="400">
<img src="static/images/miss.png" alt="Miss Screen" width="400">
<img src="static/images/in_game.png" alt="Action Gameplay" width="400">
<img src="static/images/player_2_wins.png" alt="Winner Screen" width="400">

## How to Play

1. **Select Ships:** Choose the number of ships (1-5) using the up and down arrow keys and press Enter to start.
2. **Place Ships:** Each player will place their ships on the grid. Press `R` to rotate a ship and click on the grid to place it.
3. **Take Turns:** Players take turns guessing the positions of the opponent's ships by clicking on the grid.

## Installation
- Install python 3.12 https://www.python.org/downloads/
- Open project root directory in terminal
- Initialize project environment

      python3.12 -m venv .
- Activate Project environment
    - Mac/Linux

          source bin/activate
        - NOTE: to deactivate project environment

              deactivate
        - NOTE: to reset project environment (macos, linux,)

              rm -rf bin include lib pyvenv.cfg
    - Windows Powershell

          .\Scripts\activate
        - NOTE: to deactivate project environment

              .\Scripts\deactivate.bat
        - NOTE: to reset project environment (macos, linux,)

              rm -r include
              rm -r lib 
              rm -r scripts
              rm -r pyvenv.cfg
- Install project in development mode and dependencies with PIP 

      pip install -e .
- Run on local machine
      
      python main.py

## Controls

- **Arrow Keys:** Adjust the number of ships before starting.
- **R Key:** Rotate the ship during placement.
- **Mouse Click:** Place a ship or make a guess on the opponent’s board.

## Future Improvements

- Add sound effects for hits, misses, and ship placements.
- Add AI for single-player mode against the computer.
- Improve visuals.

## Contributing

- **Coders:** Anil, Michelle, Nathan
- **Tester:** Justin
- **Documentation:** Jaret
