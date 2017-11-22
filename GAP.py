import pexpect

games_to_play=0

import signal
def ctrl_C_handler():
    games_to_play=0
signal.signal(signal.SIGINT, ctrl_C_handler)


def get_game_width(text):
    import re
    return re.search(r'\[1-(\d)\]').group(0)


def make_a_move(game_width):
    from random import choice
    return choice(range(1, game_width + 1))


def play_game():
    games_to_play
    MEFIARE = pexpect.spawn('python MEFIARE.py')
    while True:
        case = MEFIARE.expect(["Where would you like to play?", "Would you like to play another game?"])
        if case == 0:
            MEFIARE.send(make_a_move(get_game_width(MEFIARE.read())))
        if case == 1:
            


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    play_game()
    
