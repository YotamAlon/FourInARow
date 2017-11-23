import signal
ctrl_c_was_pressed = False


def ctrl_c_handler(*args):
    global ctrl_c_was_pressed
    if ctrl_c_was_pressed:
        import sys
        sys.exit(0)
    else:
        print('\nCaught ctrl-C. Stopping gracefully...')
        global games_to_play
        games_to_play = 0
        ctrl_c_was_pressed = True
signal.signal(signal.SIGINT, ctrl_c_handler)


def get_game_width(text):
    import re
    pattern = re.search(r'\[1-(\d+)\]', text).group(0)[3:-1]
    return int(pattern)


def make_a_move(game_width):
    from random import choice
    return str(choice(range(1, game_width + 1)))


def play_games(MEFIARE_args):
    import subprocess
    import time
    started = time.time()
    global games_to_play
    games_played = 0
    games_won = 0
    MEFIARE = subprocess.Popen(['python', 'MEFIARE.py', '-t'] + MEFIARE_args,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    print('Spawned MEFIARE')
    print('Now training MEFIARE for {} games'. format(games_to_play))
    while True:
        output = str(MEFIARE.stdout.readline())
        if 'next?' in output:
            MEFIARE.stdin.write(bytearray(make_a_move(get_game_width(output)) + '\n', encoding='utf-8'))
            MEFIARE.stdin.flush()
        elif 'game?' in output:
            if games_to_play == 0:
                MEFIARE.stdin.write(b'no\n')
                MEFIARE.stdin.flush()
                print('MEFIARE Done')
                print('Stats for nerds:')
                print('I played {} games, out of those, I won {} games'.format(games_played, games_won))
                print('I was running for {} seconds'.format(time.time() - started))
                break
            else:
                games_to_play -= 1
                games_played += 1
                print('Finished a game. left: {} (-1=until ctrl-C)'.format(games_to_play))
                MEFIARE.stdin.write(b'yes\n')
                MEFIARE.stdin.flush()
        elif 'You Win' in output:
            games_won += 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--games', type=int)
    parser.add_argument('-y', '--height', type=str)
    parser.add_argument('-w', '--width', type=str)
    parser.add_argument('-f', '--db-file', type=str)
    args = parser.parse_args()
    games_to_play = args.games

    MEFIARE_args = []
    if args.height is not None:
        MEFIARE_args += ['-y', args.height]
    if args.width is not None:
        MEFIARE_args += ['-w', args.width]
    if args.db_file is not None:
        MEFIARE_args += ['-f', args.db_file]
    play_games(MEFIARE_args)
    
