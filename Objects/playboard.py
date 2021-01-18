# Sogyo assignment January 2021
# Thomas Hoedeman

#Internal imports
from Objects.player import Player
from Objects.gamepiece import Gamepiece

#external imports
import matplotlib.pyplot as plt
import numpy as np
import random


class Playboard(object):
    """
    Representation of a playboard used for Tic-Tac-Toe
    """
    def __init__(self, size):
        # set size
        self.size = size

        # determine starting player
        self.next_player = random.randint(1, 2)

        # initiate game values
        self.game_over = False
        self.amount_of_games = 0

        # initiate state of the board without any gamepieces present
        self.state = {}
        for i in range(self.size * self.size):
            self.state[i+1] = '-'

        # iniate position numbers on board
        self.coords = np.zeros([self.size, self.size])
        position = 1
        for col in range(self.size):
            for row in range(self.size):
                self.coords[col][row] = position
                position+=1

        # Prompt for player names
        self.P1, self.P2 = self.players_names()

    def __str__(self):
        return self.state

    def players_names(self):
        #prompt for input
        inputP1 = []
        inputP2 = []
        while not isinstance(inputP1, str):
            inputP1 = input("What is the name of player 1?: ")
        while not isinstance(inputP2, str):
            inputP2 = input("What is the name of player 2?: ")

        #create player objects
        P1 = Player(1, inputP1)
        P2 = Player(2, inputP2)

        # check with players if input is right
        while True:
            print(f"Player 1: {inputP1}\nPlayer 2: {inputP2}")
            inp = input("Okay? press 'enter' to continue or type 'r' + enter to re-enter names: \n")
            # if enter is pressed return
            if inp == '':
                return P1, P2
            # else recursivly open new prompt for player names
            elif inp == 'r':
                P1, P2 = self.players_names()
                return P1, P2

    def empty(self):
        """
        Empty will creat an empty fullscreen window in which the board can be drawn
        """
        #remove toolbar from figures
        plt.rcParams['toolbar'] = 'None'

        #initiate figure
        self.fig = plt.figure()

        #title
        plt.title("Tic-Tac-Toe", {'fontsize': 36})

        #remove axis
        plt.axis('off')

        #full screen
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()

    def draw_board(self):
        """
        Draw_board will draw the playerboard with player names and numbers for play reference
        """

        #create empty window
        self.empty()

        #plot lines based on size of board (function also works for size > 3)
        width_coords = [x for x in range(self.size+1)]
        for i in width_coords:
            if not i == width_coords[0] and not i == width_coords[-1]:
                length_coords = [i for j in range(self.size+1)]
                plt.plot(width_coords, length_coords, 'k', linewidth=10)
                plt.plot(length_coords, width_coords, 'k', linewidth=10)

        #plot numbers that can be used as reference for input (also works for size > 3)
        for position in self.state:
                for col in range(self.size):
                    for row in range(self.size):
                        if self.coords[col, row] == position:
                            plt.text(row + 0.05, col + 0.05, str(position), {'color': 'black', 'size': 22} )

        # add player names to window
        self.P1_text = plt.text(0.15, 0.03, f"Player 1: {self.P1}", fontsize=26, c = 'r', transform=plt.gcf().transFigure)
        self.P2_text = plt.text(0.65, 0.03, f"Player 2: {self.P2}", fontsize=26,  c = 'b',transform=plt.gcf().transFigure)

        # draw a a black box around the player name that has the first turn
        self.mark_player()

    def mark_player(self):
        """
        Mark_player will show the player who has to make the next move
        """
        if self.game_over == False:
            if self.next_player == 1:
                # change the black box around playername to other player for the new turn
                self.P1_text.update({'bbox':dict(facecolor='none', edgecolor='black', pad=10.0, linewidth= 4)})
                self.P2_text.update({'bbox':dict(facecolor='none', edgecolor='white', pad=10.0, linewidth= 4)})
            elif self.next_player == 2:
                # change the black box around playername to other player for the new turn
                self.P2_text.update({'bbox':dict(facecolor='none', edgecolor='black', pad=10.0, linewidth= 4)})
                self.P1_text.update({'bbox':dict(facecolor='none', edgecolor='white', pad=10.0, linewidth= 4)})

    def play(self):
        """
        Play will allow to play a game on the playboard
        """
        # draw the board on which the game will be played
        self.draw_board()

        # print board to console (extra)
        self.print_state()

        # define response to key_press_events
        def press(event):
            # pause to prevent interference from rapid sequential respones
            plt.pause(0.2)

            # close figure on escape, backspace or q
            if event.key == 'escape' or event.key == 'backspace' or event.key == "q":
                plt.close()

            # check game status
            if self.game_over == False:
                # check if input is an number
                if event.key.isnumeric():
                    # convert to integer
                    key_press = int(event.key)
                    # check if number is a viable location on the board
                    if 0 < key_press <= self.size * self.size:

                        # call on function to perform move
                        self.turn(int(event.key), self.next_player)

                        # check if game is won or finished in a draw
                        self.check_state()

                        # swap markation of next player if not won
                        if self.game_over == False:
                            self.mark_player()

                        # print next player to console (extra)
                        if self.game_over == False:
                            print(f"Player {self.next_player} is next")

                else: # instructions as response to non-numerical input
                    message = "Press a numbered key (1-9) to place a gamepiece"
                    plt.text(0.2, 0.09, message, fontsize=20, c = 'k', transform=plt.gcf().transFigure)
                    plt.draw()

                    # pause and remove instructions after 2 seconds
                    plt.pause(2)
                    del plt.gca().texts[-1]
                    plt.draw()

            # if player responds with 'y' key press and the game is over a new game will be started
            elif event.key == 'y' and self.game_over == True:
                # clear current figure
                self.fig.clear()
                plt.draw()

                # reset board
                self.state = {}
                for i in range(self.size * self.size):
                    self.state[i+1] = '-'
                self.game_over = False

                # start new game
                self.play()

                #close old figure and update amount of games played
                plt.close(self.amount_of_games + 1)
                self.amount_of_games += 1

                # print new game to console (extra)
                print("NEW GAME")

        # starting ongoing function that will wait for key_press_events
        self.fig.canvas.mpl_connect('key_press_event', press)

        # print starting player to console (extra)
        print(f"Player {self.next_player} may start")

        # show figure
        plt.show()



    def turn(self, location, player):
        """
        Turn will make a move on the board based on player input
        """
        #Check if position is empty
        if self.state[location] == '-':

            # create game piece
            self.state[location] = Gamepiece(location, player)
            current_piece = self.state[location]

            # find coordinates of position
            for col in range(self.size):
                for row in range(self.size):
                    if self.coords[row][col] == location:

                        # draw gamepiece on the board
                        plt.plot(col + 0.5, row + 0.5, marker = current_piece.type, markersize = 100, c = current_piece.colour)
                        plt.draw()

                        # swap players (if move was made)
                        if player == 1:
                            self.next_player = 2
                        elif player == 2:
                            self.next_player = 1

                        # print next player to console (extra)
                        self.print_state()

    def print_state(self):
        """
        Print state will print the current board to the console (extra)
        """
        # flip to correspond to print orientation
        temp  = np.flip(self.coords, 0)

        # loop over state of the playboard
        for col in range(self.size):
            for row in range(self.size):
                if self.state[temp[col][row]] != '-':
                    # print gamepiece
                    print(self.state[temp[col][row]], end = "")
                else:
                    # or space
                    print(" " , end="")

                #draw vertical lines
                if row <  self.size-1:
                    print(" |", end='')

            # draw horizontal line
            if col < self.size-1:
                print("")
                print("--|--|--")
            else:
                print("")


    def check_state(self):
        """
        Check_state checks if currently the game is won or has no moves left and ends in a draw
        """
        # find arrays positions of al horizontal, vertical and diagnal lines in the playerboard
        # these functions work for playerboard size > 3 as well
        for i in range(self.size):
            # find line
            horizontal = [x+1+i*self.size for x in range(self.size)]

            # check if line is occupied by single gamepiece type
            self.check(horizontal)

            #repeat for vertical and both diagonals
            vertical = [self.size*x + 1 +i for x in range(self.size)]
            self.check(vertical)
            diag1 = [x+(x * self.size) +1 for x in range(self.size)]
            self.check(diag1)
            diag2 = [x+1+ (self.size-1)*self.size - self.size*x for x in range(self.size)]
            self.check(diag2)

        # if game is not won
        if self.game_over == False:

            # check if any position is still empty
            open_space = False
            for i in self.state:
                if self.state[i] == '-':
                    # if empty space
                    open_space = True

            # if not empty spaces left end game in draw
            if open_space == False:
                self.endgame(0)
                pass

    def check(self, array):
        """
        Checks if input line (array) is fully occupied by single gamepiece
        """
        s = self.state
        # check if not empty
        if s[array[0]] != '-' and s[array[1]] != '-' and s[array[2]] != '-':
            # check if gamepiece types are the same
            if s[array[0]].type == s[array[1]].type and s[array[1]].type == s[array[2]].type:
                # check if game was not already won
                if self.game_over == False:
                    # trigger endgame function
                    self.endgame(s[array[0]].player)

    def endgame(self, winner):
        """
        Will inform players who won and prompt for new game or quit
        """
        # change game status
        self.game_over = True

        # determine message for players to playboard and console(extra) based on win or draw
        if winner == 0:
            message = f"Game over, It was a draw, press 'q' to quit or 'y' to play again"
        if winner > 0:
            message = f"Game over, Player {winner} won, press 'q' to quit or 'y' to play again"

        # show message to console and playboard
        print(message)
        plt.text(0.15, 0.09, message, fontsize=20, c = 'k', transform=plt.gcf().transFigure)
        plt.draw()
