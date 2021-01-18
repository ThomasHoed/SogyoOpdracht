class Gamepiece(object):
    """
    Representation of a gamepiece used in Tic-Tac-Toe
    """
    def __init__(self, location, player):
        self.player = player
        if player == 1:
            self.colour = 'r'
            self.type = 'o'
        elif player == 2:
            self.colour = 'b'
            self.type = 'X'
        self.location = location

    def __str__(self):
        return self.type
