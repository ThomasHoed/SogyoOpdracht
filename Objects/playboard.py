# Sogyo assignment January 2021
# Thomas Hoedeman

#Internal imports
from Objects.player import Player
from Objects.gamepiece import Gamepiece

#external imports
import matplotlib.pyplot as plt
import numpy as np

class Playboard(object):
    """
    Representation of a playboard used for Tic-Tac-Toe
    """
    def __init__(self, size):
        self.size = size
        self.name = "Playboard on which the game is played"

        self.state = {}
        for i in range(self.size * self.size):
            self.state[i+1] = ""

        self.coords = np.zeros([self.size, self.size])
        position = 1
        for col in range(self.size):
            for row in range(self.size):
                self.coords[col][row] = position
                position+=1

        self.draw()
        self.turn()

    def __str__(self):
        return self.name

    def draw(self):
        plt.rcParams['toolbar'] = 'None'
        plt.figure()
        plt.title("Tic-Tac-Toe", {'fontsize':26})

        width_coords = [x for x in range(self.size+1)]
        for i in width_coords:
            if not i == width_coords[0] and not i == width_coords[-1]:
                length_coords = [i for j in range(self.size+1)]
                plt.plot(width_coords, length_coords, 'k', linewidth=12)
                plt.plot(length_coords, width_coords, 'k', linewidth=12)

        plt.axis('off')
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()


        plt.show()

    def turn(self, location):
        print(self.size)
        for row in range(self.size):
            for col in range(self.size):
                if self.coord[row][col] == location:
                    print(row, col)
        plt.plot(1.5, 1.5, marker = 'X', markersize = 120)
        plt.plot(0.5, 0.5, marker = 'o', markersize = 110)
