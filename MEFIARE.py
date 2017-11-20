try:
    import cpickle as pickle
except:
    import pickle

from json import dumps, loads
from random import random
from os.path import exists

game_width = 7
game_height = 6
if exists('4row.db'):
    db_file=open('4row.db', 'rb')
    db=pickle.load(db_file)
else:
    db={}


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
    # Horizontal win
    for i in range(game_width - 3):
        for j in range(game_height):
            if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]:
                return state[i][j]
    # Right leaning diagonal win
    for i in range(game_width - 3):
        for j in range(game_height - 3):
            if state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                return state[i][j]
    # Left leaning diagonal win
    for i in range(game_width - 3):
        for j in range(game_height - 3):
            if state[i][j+3] == state[i+1][j+2] == state[i+2][j+1] == state[i+3][j]:
                return state[i][j]
    return None


def propogate_game(winner, visited_states):
    for state, my_move in visited_states:
        db[state] = [chance * (1.1 - 0.2 * winner) for chance in db[state]]
        db[state][my_move] *= ((0.9 + 0.2 * winner) / (1.1 - 0.2 * winner))


def save_db():
    db_file=open('4row.db', 'wb')
    pickle.dump(db_file, db)


def play_game():
    state = [[] for i in range(game_width)]
    visited_states = []
    while True:
        print("Starting a new game:")
        while True:
            my_move = get_move_int(random(), db[dumps(state)])
            visited_states.append((dumps(state), my_move))
            state[my_move].append(1)
            print_state(state)
            winner = who_is_winner(state)
            if winner is not None: # 1 == I am winner
                propogate_game(winner, visited_states)
                break
            his_move = input("Where would you like to play? [1-%d]" % game_width)
            if len(state[his_move]) == game_height:
                print('This move is not allowed')
                continue
            winner = who_is_winner(state)
            if winner is not None: # 1 == I am winner
                propogate_game(winner, visited_states)
                break
        
        print('I Won! FeelsBadMan for you' if winner else 'You Win! Congrats')
        While True:
            another = input("Would you like to play another game? (yes/no)")
            if another in ['yes', 'no']:
                break
             print('yes or no only please.')
        
        if another == 'no':
            save_db()
            break

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Play a game of 4 In A Row against MEFIARE')
    args = parser.parse_args()
    # Add arguments when needed
    play_game()
