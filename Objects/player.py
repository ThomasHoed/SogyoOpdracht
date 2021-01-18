class Player(object):
    """
    Representation of a participant of Tic-Tac-Toe
    """
    def __init__(self, id, name):
        self.name = name
        self.id = id

    def __str__(self):
        return self.name
