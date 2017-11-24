# MEFIARE

MEFIARE (Machine Educable Four In A Row Engine) (Pronounced me-fire) is a basic AI that (with its database) is able to play Four In A Row against human players (or compatible bots).
The implementation is based on the concept of MENACE (https://en.wikipedia.org/wiki/Donald_Michie) with the database consisting of a large dictionary, with every key corresponding to a state of a game. Every value in said dict is a list of floats, which are the chances MEFIARE will play in that slot.

MEFIARE is best trained using a random bot (like GAP). In that way, no single path is selected too much, possibly causing a collapse of paths (this scenario is more possible in the original idea, that consisted selecting the path from a descrete list of possibilities, and is slightly mitigated by using a list of floats).

GAP (Generative Adverserial Player) is an automated script for playing randomly against MEFIARE.
Together, the two scripts make a complete Generative Adverserial Network. GAP is the generator, and MEFIARE is the neural network.

While MEFIARE is not coded in a similar way to other neural networks, there is a good correlation between them.

## Usage Information
To play against MEFIARE simply type in console:
```
python MEFIARE.py
```

A few command line options:
 - -t/--training-mode - do not print unnecessary information. For training purposes
 - -y/--height - the wanted height of the game (default=6)
 - -w/--width - the wanted width of the game (default=7)
 - -f/--db-file - the wanted db file to play against (default=4row.db)
 
 
 To train MEFIARE before playing against it, use the command:
 ```
 python GAP.py
 ```

Command line options:
 - -g/--games - The wanted number of games to train (default=1). Enter -1  to play indefinitely.
 - -y/--height - the wanted height of the trained game (default=6)
 - -w/--width - the wanted width of the trained game (default=7)
 - -f/--db-file - the wanted db file to train (default=4row.db)
 
Note: while playing indefinitely many games, you can stop at any time by pressing ctrl-C. GAP is supposed to exit gracefully. If it hangs, pressing ctrl-C again will forcefully exit.
