import signal
was_ctrl_c_pressed = False


def ctrl_c_handler(*args):
    global was_ctrl_c_pressed
    if was_ctrl_c_pressed:
        import sys
        sys.exit(0)
    else:
        print('\nCaught ctrl-C. Stopping gracefully...')
        global games_to_play
        games_to_play = 0
        was_ctrl_c_pressed = True
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
    MEFIARE = subprocess.Popen(['python', 'MEFIARE.py'] + MEFIARE_args,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN))
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
    parser.add_argument('-g', '--games', type=int, default=1)
    parser.add_argument('-y', '--height', type=str, default='6')
    parser.add_argument('-w', '--width', type=str, default='7')
    parser.add_argument('-f', '--db-file', type=str, default='4row.db')
    args = parser.parse_args()
    games_to_play = args.games
    play_games(['-y', args.height, '-w', args.width, '-f', args.db_file])
    
