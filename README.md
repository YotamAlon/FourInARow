# FourInARow

This script (with its database) will be able to play Four In A Row against human players (or compatible bots).
The implementation is based on the concept of MENACE (https://en.wikipedia.org/wiki/Donald_Michie) with the database consisting of a large dictionary, with every key corresponding to a state of a game. Every value in said dict is a list of floats, which are the chances MEFIARE will play in that slot.

The MEFIARE (Machine Educable Four In A Row Engine) is best trained using a random bot. In That way no 
