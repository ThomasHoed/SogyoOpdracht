class Player(object):
    """
    Representation of a participant of Tic-Tac-Toe
    """
    def __init__(self, name):
        self.name = name
        self.wins = 0

    def __str__(self):
        return self.name
