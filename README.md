# MEFIARE

MEFIARE (Machine Educable Four In A Row Engine) (Pronounced me-fire) is a basic AI that (with its database) is able to play Four In A Row against human players (or compatible bots).
The implementation is based on the concept of MENACE (https://en.wikipedia.org/wiki/Donald_Michie) with the database consisting of a large dictionary, with every key corresponding to a state of a game. Every value in said dict is a list of floats, which are the chances MEFIARE will play in that slot.

MEFIARE is best trained using a random bot. In that way, no single path is selected too much, possibly causing a collapse of paths (this scenario is more possible in the original idea, that consisted selecting the path from a descrete list of possibilities, and is slightly mitigated by using a list of floats).
