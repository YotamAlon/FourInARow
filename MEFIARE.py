try:
    import cpickle as pickle
except:
    import pickle

from json import dumps, loads
from random import random
game_width = 7
game_height = 6
db_file=open('4row.db', 'rb')
db=pickle.load(db_file)


def get_move_int(rand, chances):
    for i in range(len(chances)):
        if sum(chances[:i+1]) > rand:
            return i


def print_state(state):
    for i in range(len(state)):
        print('|'.join(state[i]))


def who_is_winner(state):
    # Vertical win
    for i in range(game_width):
        for j in range(game_height - 3):
            if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3]:
                return state[i][j]
    for i in range(game_width - 3):
        # Horizontal win
        for j in range(game_height):
            if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]:
                return state[i][j]


def play_game():
    state = [[] for i in range(game_width)]
    visited_states = []
    my_move = get_move_int(random(), db[dumps(state)])
    visited_states.append((dumps(state), my_move))
    state[my_move].append(1)

    while True:
        print_state(state)
        his_move = input("Where would you like to play? [1-%d]" % game_width)
        if len(state[his_move]) == game_height:
            print('This move is not allowed')
            continue
        state
        winner = who_is_winner(state)
