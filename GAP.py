import pexpect

games_to_play=0

import signal
def ctrl_C_handler(*args):
    print('\nCaught ctrl-C with args: ' + str(args))
    global games_to_play
    games_to_play=0
signal.signal(signal.SIGINT, ctrl_C_handler)


def get_game_width(text):
    print("Text: \n {}".format(text))
    import re
    pattern = re.search(r'\[1-(\d)\]', text).group(0)
    print('Got {} from {}'.format(pattern, text))
    return pattern


def make_a_move(game_width):
    from random import choice
    return choice(range(1, game_width + 1))


def play_game():
    global games_to_play
    MEFIARE = pexpect.spawn('python MEFIARE.py', encoding='utf-8')
    print('Spawned MEFIARE')
    import time
    while True:
        case = MEFIARE.expect(['X', r'g', pexpect.EOF])
        print(MEFIARE.read())
        if case == 0:
            MEFIARE.sendline(make_a_move(get_game_width(MEFIARE.read())))
        if case == 1:
            if games_to_play == 0:
                MEFIARE.send('no\n')
                MEFIARE.expect(pexpect.EOF)
                print('MEFIARE ended')
            else:
                print('Finished a game. left: {} (-1=until ctrl-C)'.format(games_to_play))
                games_to_play -= 1
                MEFIARE.send('yes\n')
        if case == 2:
            print('MEFIARE exited unexpectedly')
            break


def play_game2():
    import subprocess
    import time
    global games_to_play
    MEFIARE = subprocess.Popen(['python', 'MEFIARE.py'], stdout=subprocess.PIPE)
    output = MEFIARE.output.read()[-50:]
    while True:
        if 'next' in output:
            output = MEFIARE.communicate(make_a_move(get_game_width(output)))[0]
        elif 'game' in output:
            if games_to_play == 0:
                output = MEFIARE.communicate('no\n')[0]
                print('MEFIARE exited')
                break
            else:
                print('Finished a game. left: {} (-1=until ctrl-C)'.format(games_to_play))
                games_to_play -= 1
                output = MEFIARE.communicate('yes\n')[0]
        else:
            print(output)
            print('Unknown error occurred')
            break


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    play_game2()
    
