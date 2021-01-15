class Gamepiece(object):
    """
    Representation of a gamepiece used in Tic-Tac-Toe
    """
    def __init__(self, type, player):
        self.type = type
        self.owner = player

    def __str__(self):
        return self.type, " owned by ", self.owner
