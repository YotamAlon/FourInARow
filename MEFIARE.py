import pymongo
from json import dumps
from random import random
from os.path import exists


class DBHandler(object):
    host = 'localhost'
    port = 27017
    db_name = 'four_row_db'
    collection_name = 'default'
    collection = None
    meta_attrs = {'games': 0}
    cache = {}
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        from pymongo import MongoClient
        client = MongoClient()
        self.collection = client[self.db_name][self.collection_name]
        if 'state' not in self.collection.index_information():
            self.collection.create_index('state')
        if self.collection.find_one({'state': 'meta'}) is None:
            self.collection.insert_one({**{'state': 'meta'}, **self.meta_attrs})
    
    def __getitem__(self, key):
        if key in self.cache:
            return self.cache[key]
        elif key in self.meta_attrs:
            value = self.collection.find_one({'state': 'meta'})
            return value[key]
        else:
            value = self.collection.find_one_and_update(
                {'state': key}, 
                {'$setOnInsert': {
                    'state': key,
                    'chances': [1. / game_width for i in range(game_width)]}},
                upsert=True,
                return_document=pymongo.ReturnDocument.AFTER)
            return value['chances']
    
    def __setitem__(self, key, value):
        self.cache[key] = value
    
    def __iadd__(self, inc):
        if 'games' not in self.cache:
            self.cache['games'] = self.collection.find_one({'state': 'meta'})['games']
        self.cache['games'] += 1
    
    def save(self):
        from pymongo import UpdateOne
        requests = []
        for key in self.cache:
            if key not in self.meta_attrs:
                requests.append(UpdateOne(
                    {'state': key}, 
                    {'$set': {'state': key,
                              'chances': self.cache[key]}},
                    upsert=True))
        requests.append(UpdateOne(
            {'state': 'meta'},
            {'$set': {key: self.cache[key] for key in self.meta_attrs 
                      if key in self.cache}}, upsert=True))
        self.collection.bulk_write(requests, ordered=False)
        

def load_db():
    db = DBHandler(collection_name=db_collection_name)
    return db
    

def get_move_int(rand, db, state):
    db[state] = [1. / game_width for i in range(game_width)]
    for i in range(game_width):
        if sum(db[state][:i+1]) > rand:
            return i+1


def print_state(state):
    print('|'.join([str(i+1) for i in range(game_width)]))
    for i in range(game_height - 1, -1, -1):
        print('|'.join([('X' if state[j][i] else 'O')
                        if len(state[j]) > i else ' '
                        for j in range(game_width)]))


def who_is_winner(state):
    # Vertical win
    if all([len(column) == game_height for column in state]):
        return 2
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


def propogate_game(winner, visited_states, db):
    db['games'] += 1
    for state, my_move in visited_states:
        db[state] = [chance * (1.1 - 0.2 * winner) for chance in db[state]]
        db[state][my_move-1] *= ((0.9 + 0.2 * winner) / (1.1 - 0.2 * winner))
        state_sum = sum(db[state])
        db[state] = [pos / state_sum for pos in db[state]]


def save_db(db):
    db.save()
    
    
def play_game(training_mode):
    db = load_db()
    while True:
        state = [[] for i in range(game_width)]
        visited_states = []
        if not training_mode:
            print("Starting a new game:")
        while True:
            # I make my move
            while True:
                my_move = get_move_int(random(), db, dumps(state))
                if len(state[my_move-1]) < game_height:
                    break
            visited_states.append((dumps(state), my_move))
            state[my_move-1].append(1)
            if not training_mode:
                print_state(state)
            
            # Check if I am the winner
            winner = who_is_winner(state)
            if winner is not None:  # 1 == I am winner
                break
            
            # Now you make your move
            while True:
                try:
                    his_move = int(input("Where would you like to play next? [1-%d]\n >> " % game_width))
                except ValueError:
                    print('Please select one of the numbers specified.')
                    continue
                if 1 <= his_move <= game_width and len(state[his_move-1]) < game_height:
                    break
                print('This move is not allowed')
            state[his_move-1].append(0)
            
            # Check if you are the winner
            winner = who_is_winner(state)
            if winner is not None:  # 1 == I am winner
                break
        
        # Print game result
        if winner in [0, 1]:
            print('I Won! FeelsBadMan for you' if winner else 'You Win! Congrats')
            propogate_game(winner, visited_states, db)
        else:
            print('This is a tie!')
        
        # Do you want to play another?
        while True:
            another = input("Would you like to play another game? (yes/no)\n >> ")
            if another in ['yes', 'no']:
                break
            print('yes or no only please.')
        
        # If no, exit. If yes, restart the loop
        if another == 'no':
            db.save()
            break

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Play a game of 4 In A Row against MEFIARE')
    parser.add_argument('-t', '--training-mode', action='store_true', default=False)
    parser.add_argument('-y', '--height', type=int, default=6)
    parser.add_argument('-w', '--width', type=int, default=7)
    parser.add_argument('-c', '--db-collection', type=str, default='4row')
    args = parser.parse_args()

    game_width = args.width
    game_height = args.height
    db_collection_name = args.db_collection
    if args.training_mode:
        import signal
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    play_game(args.training_mode)
    
