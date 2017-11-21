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


def get_move_int(rand, db, state):
    if state not in db:
        db[state] = [1. / game_width for i in range(game_width)]
    for i in range(game_width):
        if sum(db[state][:i+1]) > rand:
            return i


def print_state(state):
    for i in range(game_height - 1, -1, -1):
        print('|'.join([str(state[j][i])
                        if len(state[j]) > i else '-'
                        for j in range(game_width)]))


def who_is_winner(state):
    # Vertical win
    for i in range(game_width):
        for j in range(game_height - 3):
            try:
                if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3]:
                    return state[i][j]
            except IndexError:
                pass
    # Horizontal win
    for i in range(game_width - 3):
        for j in range(game_height):
            try:
                if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]:
                    return state[i][j]
            except IndexError:
                pass
    # Right leaning diagonal win
    for i in range(game_width - 3):
        for j in range(game_height - 3):
            try:
                if state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return state[i][j]
            except IndexError:
                pass
    # Left leaning diagonal win
    for i in range(game_width - 3):
        for j in range(game_height - 3):
            try:
                if state[i][j+3] == state[i+1][j+2] == state[i+2][j+1] == state[i+3][j]:
                    return state[i][j]
            except IndexError:
                pass
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
            my_move = get_move_int(random(), db, dumps(state))
            visited_states.append((dumps(state), my_move))
            state[my_move].append(1)
            print_state(state)
            winner = who_is_winner(state)
            if winner is not None: # 1 == I am winner
                propogate_game(winner, visited_states)
                break
            while True:
                try:
                    his_move = int(input("Where would you like to play? [1-%d]\n >> " % game_width))
                except ValueError:
                    print('Please select one of the numbers specified.')
                    continue
                if his_move - 1 < game_width and len(state[his_move-1]) < game_height:
                    break
                print('This move is not allowed')
                    
            state[his_move-1].append(0)
            winner = who_is_winner(state)
            if winner is not None: # 1 == I am winner
                propogate_game(winner, visited_states)
                break
        
        print('I Won! FeelsBadMan for you' if winner else 'You Win! Congrats')
        while True:
            another = input("Would you like to play another game? (yes/no)\n >> ")
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
