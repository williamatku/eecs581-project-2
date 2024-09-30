import logging
from src.game import start_game

if __name__ == "__main__":
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)
    start_game()
