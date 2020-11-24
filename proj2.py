"""
File:    proj2.py
Author:  Deborah Miller
Date:    04/22/2020
Section: 14
E-mail:  d169@umbc.edu
Description:
  connect four, against another player or against the computer
four in a row in any direction wins
you get to choose what game boards to upload
you can even save your game and continue a different time
extra credit: the computer will try to win and block you from winning!
"""
from random import randint


class AdjoinTheSpheres:

    def __init__(self):
        self.ok_choices = [1, 2, 3]
        self.game_board = []
        self.current_board = []

        # starts with boolean set to true bec x goes first
        self.x_or_o = True
        self.x_or_comp = True
        self.DOUBLE = 2
        self.WIN = 4
        self.stop = False
        

    def main_menu(self):
        """
        function gives the user the game menu options,
        and makes sure you only choose one of these three
        sends the option chosen to game play
        """
        print("AdjoinTheSpheres Main Menu \n",
              "1) New Game (2 player) \n",
              "2) New Game (1 player vs computer)\n",
              "3) Exit Game")

        self.options = int(input("Select Option from the Menu: "))

        while self.options not in self.ok_choices:
            print("Invalid choice, try again.")
            self.main_menu()

        if self.options == 1 or self.options == 2:
            self.play(self.options)

    def play(self, options):
        """
        :param options: play against another player or the computer
        :return: none but most of the game play takes place in here, sending information
        to different functions
        """

        # asks what game to load then loads that game
        self.game_map = input("What game/map do you want to load? ")
        
        self.current_board = self.load_game(self.game_map)
        
        # if no winner yet, keep playing
        while not self.check(self.current_board[1]):

            # sees if it's x or o turn
            # true means it's x
            if self.x_or_o:
                next_player = 'x'

                # changes to the next player's turn here so when x finishes going, it'll be ready
                self.x_or_o = False

            elif not self.x_or_o:
                if options == 1:
                    next_player = 'o'
                elif options == 2:
                    next_player = 'computer'

                # changes to the next player's turn
                self.x_or_o = True

            if next_player != 'computer':

                # prompt for what you can do during your turn
                self.turn = input("Player " + next_player + " What move do you want to make?  "
                                                            "Answer as row (horizontal) column (vertical) "
                                                            "or save game or load game ")

                if self.turn.lower() == "save game":
                    save_as = input("What would you like to save the game as? ")
                    self.save(save_as, self.current_board[1])

                elif self.turn.lower() == "load game":
                    
                    self.play(options)
                    self.stop = True

                else:
                    # send the two numbers to the move function to make it happen
                    row = self.turn.split()[0]
                    column = self.turn.split()[1]
                    self.current_board = self.move(self.current_board[1], next_player, row, column)

                # if it was an illegal move, function starts again
                while not self.current_board[0]:

                    print("illegal move")

                    self.turn = input("Player " + next_player + " What move do you want to make?  "
                                                                "Answer as row (horizontal) column (vertical) "
                                                                "or save game or load game ")

                    if self.turn.lower() == "save game":
                        save_as = input("What would you like to save the game as? ")
                        self.save(save_as, self.current_board[1])
                        self.current_board[0] = True

                    elif self.turn.lower() == "load game":
                        self.play(options)
                        self.current_board[0] = True
                        self.stop = True

                    else:
                        row = self.turn.split()[0]
                        column = self.turn.split()[1]
                        self.current_board = self.move(self.current_board[1], next_player, row, column)

            # if it's the computer's turn
            else:
                self.turn = self.computer_turn(self.current_board[1])
                
                # add one bec the board starts at zero but the player will start at one
                row = int(self.turn[0]) + 1
                column = int(self.turn[1]) + 1
                self.current_board = self.move(self.current_board[1], 'o', row, column)
                
                # if the random generator gave an illegal move
                while not self.current_board[0]:
                    self.turn = self.computer_turn(self.current_board[1])
                    row = int(self.turn[0]) + 1
                    column = int(self.turn[1]) + 1
                    self.current_board = self.move(self.current_board[1], 'o', row, column)
        if self.stop:
            self.stop = False
        else:
            # once the board is filled, see if there's a winner or a tie
            if self.check(self.current_board[1]) == "tie":
                print("Tie Game")

                # if there's a winner
            else:
                if not self.x_or_o:
                    next_player = 'x'
                elif self.x_or_o:
                    if options == 1:
                        next_player = 'o'
                    elif options == 2:
                        next_player = 'computer'

                print("The winner is player", next_player)

            self.print_board(self.current_board[1])

            # goes back to the main menu
            self.main_menu()

    def computer_turn(self, current_board):
        """
        extra credit!
        :param: current_board
        :return: if there's somewhere to go for the computer to win or block opponants win, 
        it will return that row and column numbers as a list there, other wise 2 random numbers are generated
        """
        row = current_board[0][0]
        column = current_board[0][1]
        board = current_board[2]

        # check vertical
        for i in range(int(row)):
            for j in range(int(column)):
                
                if board[i][j] == "x" and i <= int(row) - self.WIN and board[i + 1][j] == "x" \
                        and board[i + 2][j] == "x":

                    if board[i + 3][j] == " ":
                        row = i + 3
                        column = j
                        return [row, column]

                    elif i != 0 and board[i - 1][j] == " ":
                        row = i - 1
                        column = j
                        return [row, column]

                elif board[i][j] == "x" and i <= int(row) - self.WIN and board[i + 1][j] == "x" \
                        and board[i + 3][j] == "x" and board[i + 2][j] == " ":
                    row = i + 2
                    column = j
                    return [row, column]

                elif board[i][j] == "x" and i <= int(row) - self.WIN and board[i + 2][j] == "x" \
                        and board[i + 3][j] == "x" and board[i + 1][j] == " ":
                    row = i + 1
                    column = j
                    return [row, column]

                elif board[i][j] == " " and i == int(row) - self.WIN and board[i + 1][j] == "x" \
                        and board[i + 2][j] == "x" and board[i + 3][j] == "x":
                    row = i
                    column = j
                    return [row, column]

                elif board[i][j] == "o" and i <= int(row) - self.WIN and board[i + 1][j] == "o" \
                        and board[i + 2][j] == "o":
                    if board[i + 3][j] == " ":
                        row = i + 3
                        column = j
                        return [row, column]

                    elif i != 0 and board[i - 1][j] == " ":
                        row = i - 1
                        column = j
                        return [row, column]

                elif board[i][j] == "o" and i <= int(row) - self.WIN and board[i + 1][j] == "o" \
                        and board[i + 3][j] == "o" and board[i + 2][j] == " ":
                    row = i + 2
                    column = j
                    return [row, column]

                elif board[i][j] == "o" and i <= int(row) - self.WIN and board[i + 2][j] == "o" \
                        and board[i + 3][j] == "o" and board[i + 1][j] == " ":
                    row = i + 1
                    column = j
                    return [row, column]

                elif board[i][j] == " " and i == int(row) - self.WIN and board[i + 1][j] == "o" \
                        and board[i + 2][j] == "o" and board[i + 3][j] == "o":
                    row = i
                    column = j
                    return [row, column]

        # check horizontal
        for i in range(int(row)):
            for j in range(int(column)):

                if board[i][j] == "x" and j <= int(column) - self.WIN and board[i][j + 1] == "x" \
                        and board[i][j + 2] == "x":

                    if board[i][j + 3] == " ":
                        row = i
                        column = j + 3
                        return [row, column]

                    elif j != 0 and board[i][j - 1] == " ":
                        row = i
                        column = j - 1
                        return [row, column]

                elif board[i][j] == "x" and j <= int(column) - self.WIN and board[i][j + 1] == "x" \
                        and board[i][j + 3] == "x" and board[i][j + 2] == " ":
                    row = i
                    column = j + 2
                    return [row, column]

                elif board[i][j] == "x" and j <= int(column) - self.WIN and board[i][j + 2] == "x" \
                        and board[i][j + 3] == "x" and board[i][j + 1] == " ":
                    row = i
                    column = j + 1
                    return [row, column]

                elif board[i][j] == " " and j == int(column) - self.WIN and board[i][j + 1] == "x" \
                        and board[i][j + 2] == "x" and board[i][j + 3]:
                    row = i
                    column = j + 2
                    return [row, column]

                elif board[i][j] == "o" and j <= int(column) - self.WIN and board[i][j + 1] == "o" \
                        and board[i][j + 2] == "o":

                    if board[i][j + 3] == " ":
                        row = i
                        column = j + 3
                        return [row, column]

                    elif j != 0 and board[i][j - 1] == " ":
                        row = i
                        column = j - 1
                        return [row, column]

                elif board[i][j] == "o" and j <= int(column) - self.WIN and board[i][j + 1] == "o" \
                        and board[i][j + 3] == "o" and board[i][j + 2] == " ":
                    row = i
                    column = j + 2
                    return [row, column]

                elif board[i][j] == "o" and j <= int(column) - self.WIN and board[i][j + 2] == "o" \
                        and board[i][j + 3] == "o" and board[i][j + 1] == " ":
                    row = i
                    column = j + 1
                    return [row, column]

                elif board[i][j] == " " and j == int(column) - self.WIN and board[i][j + 1] == "o" \
                        and board[i][j + 2] == "o" and board[i][j + 3] == "o":
                    row = i
                    column = j
                    return [row, column]

        # check diagonal
        for i in range(int(row)):
            for j in range(int(column)):

                if board[i][j] == "x" and i <= int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 1][j + 1] == "x" and board[i + 2][j + 2] == "x":

                    if board[i + 3][j + 3] == " ":
                        row = i + 3
                        column = j + 3
                        return [row, column]

                    elif i != 0 and j != 0 and board[i - 1][j - 1] == " ":
                        row = i - 1
                        column = j - 1
                        return [row, column]

                elif board[i][j] == "x" and i <= int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 1][j + 1] == "x" and board[i + 3][j + 3] == "x" and board[i + 2][j + 2] == " ":
                    row = i + 2
                    column = j + 2
                    return [row, column]

                elif board[i][j] == "x" and i <= int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 2][j + 2] == "x" and board[i + 3][j + 3] == "x" and board[i + 1][j + 1] == " ":
                    row = i + 1
                    column = j + 1
                    return [row, column]

                elif board[i][j] == " " and i <= int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 1][j + 1] == "x" and board[i + 2][j + 2] == "x" and board[i + 3][j + 3] == "x":
                    row = i
                    column = j
                    return [row, column]

                elif board[i][j] == "o" and i <= int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 1][j + 1] == "o" and board[i + 2][j + 2] == "o":

                    if board[i + 3][j + 3] == " ":
                        row = i + 3
                        column = j + 3
                        return [row, column]

                    elif i != 0 and j != 0 and board[i - 1][j - 1] == " ":
                        row = i - 1
                        column = j - 1
                        return [row, column]

                elif board[i][j] == "o" and i <= int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 1][j + 1] == "o" and board[i + 3][j + 3] == "o" and board[i + 2][j + 2] == " ":
                    row = i + 2
                    column = j + 2
                    return [row, column]

                elif board[i][j] == "o" and i <= int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 2][j + 2] == "o" and board[i + 3][j + 3] == "o" and board[i + 1][j + 1] == " ":
                    row = i + 1
                    column = j + 1
                    return [row, column]

                elif board[i][j] == " " and i == int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 1][j + 1] == "o" and board[i + 2][j + 2] == "o" and board[i + 3][j + 3] == "o":
                    row = i
                    column = j
                    return [row, column]


        # check anti-diagonal 
        for i in range(int(row)):
            for j in range(int(column)):

                if j - 3 > -1:
                    if board[i][j] == "x" and i <= int(row) - self.WIN \
                            and board[i + 1][j - 1] == "x" and board[i + 2][j - 2] == "x":

                        if board[i + 3][j - 3] == " ":
                            row = i + 3
                            column = j - 3
                            return [row, column]

                        elif i != 0 and j != int(row) and board[i - 1][j + 1] == " ":
                            row = i - 1
                            column = j + 1
                            return [row, column]

                    elif board[i][j] == "x" and i <= int(row) - self.WIN \
                            and board[i + 2][j - 2] == "x" and board[i + 3][j - 3] == "x" and board[i + 1][j - 1] == " ":
                        row = i + 1
                        column = j - 1
                        return [row, column]

                    elif board[i][j] == "x" and i <= int(row) - self.WIN \
                            and board[i + 1][j - 1] == "x" and board[i + 3][j - 3] == "x" and board[i + 2][j - 2] == " ":
                        row = i + 2
                        column = j - 2
                        return [row, column]

                    elif board[i][j] == " " and i == int(row) - self.WIN \
                            and board[i + 1][j - 1] == "x" and board[i + 2][j - 2] == "x" and board[i + 3][j - 3] == "x":
                        row = i
                        column = j
                        return [row, column]

                    elif board[i][j] == "o" and i <= int(row) - self.WIN \
                            and board[i + 1][j - 1] == "o" and board[i + 2][j - 2] == "o":

                        if board[i + 3][j - 3] == " ":
                            row = i + 3
                            column = j - 3
                            return [row, column]

                        elif i != 0 and j != int(row) and board[i - 1][j + 1] == " ":
                            row = i - 1
                            column = j + 1
                            return [row, column]

                    elif board[i][j] == "o" and i <= int(row) - self.WIN <= j \
                            and board[i + 2][j - 2] == "o" and board[i + 3][j - 3] == "o" and board[i + 1][j - 1] == " ":
                        row = i + 1
                        column = j - 1
                        return [row, column]

                    elif board[i][j] == "o" and i <= int(row) - self.WIN \
                            and board[i + 1][j - 1] == "o" and board[i + 3][j - 3] == "o" and board[i + 2][j - 2] == " ":
                        row = i + 2
                        column = j - 2
                        return [row, column]

                    elif board[i][j] == " " and i == int(row) - self.WIN \
                            and board[i + 1][j - 1] == "o" and board[i + 2][j - 2] == "o" and board[i + 3][j - 3] == "o":
                        row = i
                        column = j
                        return [row, column]
                    
        # no potential win, so generate random number 0 - lengths of the width and height of board
        row = randint(0, int(current_board[0][0]) - 1)
        column = randint(0, int(current_board[0][1]) - 1)

        return [row, column]

    def load_game(self, game_map):
        """
        :param: game_map, the specific game board the player want to use
        :return: list: [[row, column], x or o, [[row],
                                                [row],
                                                [row]]]
        """
        self.game_board = []
        first_index = []
        last_index = []
        board = []

        with open(game_map) as game:
            for number in game.readline().strip():

                # appends the row and column numbers as a list to the game board
                if number != " ":
                    first_index.append(number)
            self.game_board.append(first_index)

            # append the x or o to the list
            x_or_o = game.readlines(1)
            for x_or_o in x_or_o:
                x_or_o = x_or_o.strip()
            self.game_board.append(x_or_o)

            # append the board to the overall game board
            for line in game.readlines():
                
                board = []
                for symbol in line:
                    
                    if symbol != "\n":
                        board.append(symbol)
                    while symbol == "\n" and len(board) < int(first_index[1]):
                        board.append(" ")

                last_index.append(board)

            # if the board is blank
            if not game.readlines() and len(board) < int(first_index[0]):
                
                for i in range(int(first_index[0])):
                    board = []
                    for j in range(int(first_index[1])):
                        while len(board) < int(first_index[1]):
                            board.append(" ")
                    last_index.append(board)
            
        self.game_board.append(last_index)
        self.print_board(self.game_board)
        
        return [True, self.game_board]

    def save(self, save_as, current_board):
        """
        :param: save_as, file name the user wants the board saved as
        :param: current_board, the current board
        :return: none, but saves the current game board under a specific name, then the game continues
        """
        with open(save_as, 'w') as saving:
            board = current_board[2]
            row = current_board[0][0]
            column = current_board[0][1]

            saving.write(row + " " + column + '\n')
            saving.write(current_board[1])

            for i in range(int(row)):
                saving.write('\n')
                for j in range(int(column)):
                    saving.write(board[i][j])

    def move(self, current_board, next_turn, row, column):
        """
        :param: current_board, the current board
        :param: next_turn, who's turn it is
        :param: row what row the user wants to go to
        :param: column, what column the user wants to go
        :return: either the new board or a list of False and the unchanged board, if the move was illegal
        put x or o in right position
        if can't go there (bec something else already there or was given non existent column and row), return false
        else, send the board to the print function
        """
        board = current_board[2]

        if int(column) > int(current_board[0][1]) or int(column) < 1 or \
                int(row) > int(current_board[0][0]) or int(row) < 1:
            return [False, current_board]

        elif board[int(row) - 1][int(column) - 1] != " ":
            return [False, current_board]

        else:
            board[int(row) - 1][int(column) - 1] = next_turn

        self.print_board(current_board)
        return [True, current_board]

    def check(self, current_board):
        """
        :param: current_board, the current board
        :return: True, False or tie
        checks to see if the current board has a win, if so returns true
        also checks if it's a tie game
        """
        row = current_board[0][0]
        column = current_board[0][1]
        board = current_board[2]
        tie_maybe = []

        # check vertical win
        for i in range(int(row)):
            for j in range(int(column)):
                if board[i][j] == "x" and i <= int(row) - self.WIN and board[i + 1][j] == "x" \
                        and board[i + 2][j] == "x" and board[i + 3][j] == "x":
                    return True

                elif board[i][j] == "o" and i <= int(row) - self.WIN and board[i + 1][j] == "o" \
                        and board[i + 2][j] == "o" and board[i + 3][j] == "o":
                    return True

        # check for horizontal win
        for i in range(int(row)):
            for j in range(int(column)):
                if board[i][j] == "x" and j <= int(column) - self.WIN and board[i][j + 1] == "x" \
                        and board[i][j + 2] == "x" and board[i][j + 3] == "x":
                    return True

                elif board[i][j] == "o" and j <= int(column) - self.WIN and board[i][j + 1] == "o" \
                        and board[i][j + 2] == "o" and board[i][j + 3] == "o":
                    return True

        # check for diagonal win
        for i in range(int(row)):
            for j in range(int(column)):
                if board[i][j] == "x" and i <= int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 1][j + 1] == "x" and board[i + 2][j + 2] == "x" and board[i + 3][j + 3] == "x":
                    return True

                elif board[i][j] == "o" and i <= int(row) - self.WIN and j <= int(column) - self.WIN \
                        and board[i + 1][j + 1] == "o" and board[i + 2][j + 2] == "o" and board[i + 3][j + 3] == "o":
                    return True

        # check for anti-diagonal win
        for i in range(int(row)):
            for j in range(int(column)):
                if board[i][j] == "x" and i <= int(row) - self.WIN \
                        and board[i + 1][j - 1] == "x" and board[i + 2][j - 2] == "x" and board[i + 3][j - 3] == "x":
                    return True

                elif board[i][j] == "o" and i <= int(row) - self.WIN \
                        and board[i + 1][j - 1] == "o" and board[i + 2][j - 2] == "o" and board[i + 3][j - 3] == "o":
                    return True

        # check for tie game
        for i in range(int(row)):
            for j in range(int(column)):
                tie_maybe.append(board[i][j])

        if " " not in tie_maybe:
            return "tie"

        return False

    def print_board(self, current_board):
        """
        :param: current_board, the current board
        :return: none but prints the current board with
        the current spaces and numbers and lines...
        """
        the_numbers = []
        board = current_board[2]
        
        # prints the numbers at the top
        for i in range(1, int(current_board[0][1]) + 1):
            if i == 1:
                print("  " + str(i) + "|", end="")

            elif i == int(current_board[0][1]):
                print(str(i), end="")

            else:
                print(str(i) + "|", end="")
        print()

        # prints the board, each line is numbered, each column is joined together by |,
        # and each row is separated by --
        for i in range(len(board)):
            print(" ", '-' * int(current_board[0][1]) * self.DOUBLE)
            print(i + 1, "|".join(board[i]))

        print(" ", '-' * int(current_board[0][1]) * self.DOUBLE)

if __name__ == "__main__":
        
    play_game = AdjoinTheSpheres()
    play_game.main_menu()
