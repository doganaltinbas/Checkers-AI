from copy import deepcopy
from termcolor import colored
import numpy as np
from scipy import ndimage
import math
import matplotlib.pyplot as plt

p1_str = ""
p2_str = ""

def getOpponentColor(color):
    # Returns the opposing color 'o' or 'x'

    if color.lower() == 'x':
        return 'o'
    elif color.lower() == 'o':
        return 'x'
    else:
        return ' '


def isCapturePossibleFromPosition(board, x, y, color):

    if board[x][y] == color.upper():
        i = 5
        while i >= 2:
            if canKingMoveToPosition(board, x, y, x - i, y - i, "nw"):
                print("from",x,y,"to",x-i,y-i)
                return True
            if canKingMoveToPosition(board, x, y, x - i, y + i, "ne"):
                print("from",x,y,"to",x-i,y+i)
                return True
            if canKingMoveToPosition(board, x, y, x + i, y - i, "sw"):
                print("from",x,y,"to",x+i,y-i)
                return True
            if canKingMoveToPosition(board, x, y, x + i, y + i, "se"):

                print("from",x,y,"to",x+i,y+i)
                return True
            i = i - 1
        return False




    # Returns whether (x,y) piece can make a capture at this time

    # Check whether a jump possible to all four directions
    if canMoveToPosition(board, x, y, x - 2, y - 2):
        return True
    if canMoveToPosition(board, x, y, x - 2, y + 2):
        return True
    if canMoveToPosition(board, x, y, x + 2, y - 2):
        return True
    if canMoveToPosition(board, x, y, x + 2, y + 2):
        return True

    return False


def isCapturePossible(board, color):
    # Returns whether any of the <color> pieces can make a capture at this time

    # Loop through all board positions
    for piece in range(1, 25):
        xy = serialToGrid(piece)
        x = xy[0]
        y = xy[1]

        # Check whether this board position is our color
        if board[x][y].upper() == color.upper():
            if isCapturePossibleFromPosition(board, x, y, color):
                return True

    return False


def doMovePosition(board, x1, y1, x2, y2):
    # Will alter the board, may need to make a deepcopy() before calling this function
    # Will perform the move action
    # The move can be a simple move or a capture (but not multiple capture)
    # Make sure to call canMoveToPosition()/isLegalMove()
    # 	before this function to make sure this move is legal
    # Returns True/False, if it is a capture move or not

    isCapture = False

    board[x2][y2] = board[x1][y1]
    board[x1][y1] = ' '

    if abs(x1 - x2) >= 2:  # It's a capture move
        direction = ""
        if x2 < x1 and y2 < y1:
            board[x2 + 1][y2 + 1] = ' '
        elif x2 < x1 and y2 > y1:
            board[x2 + 1][y2 - 1] = ' '
        elif x2 > x1 and y2 < y1:
            board[x2 - 1][y2 + 1] = ' '
        elif x2 > x1 and y2 > y1:
            board[x2 - 1][y2 - 1] = ' '
        isCapture = True

    if x2 == 0 or x2 == 7:
        # Make it a king, even if it already is a king, we don't care
        board[x2][y2] = board[x2][y2].upper()

    return isCapture


def doMove(board, move):
    # Will alter the board, may need to make a deepcopy() before calling this function
    # Will perform all the move actions from the move list
    # Make sure to call isLegalMove() before this function to make sure this move is legal

    # Get the starting move position
    xy = serialToGrid(move[0])
    x1 = xy[0]
    y1 = xy[1]

    # Loop through 2nd to last items on the move list
    for i in range(1, len(move)):
        xy = serialToGrid(move[i])
        x2 = xy[0]
        y2 = xy[1]

        # Perform the move
        _ = doMovePosition(board, x1, y1, x2, y2)

        # Preparing for next loop
        x1 = x2
        y1 = y2


def canMoveToPosition(board, x1, y1, x2, y2):
    # Check whether (x1,y1) can move to (x2,y2) in one move (plain or capture)

    if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x1 > 7 or y1 > 5 or x2 > 7 or y2 > 5:
        return False

    color = board[x1][y1]
    if color == ' ':
        return False
    if board[x2][y2] != ' ':
        return False
    x1_x2 = abs(x1 - x2)
    y1_y2 = abs(y1 - y2)
    if x1_x2 != 1 and x1_x2 != 2:
        return False
    if x1_x2 != y1_y2:
        return False
    if color == 'o' and x2 > x1:  # o men cannot move down
        return False
    if color == 'x' and x2 < x1:  # x men cannot move up
        return False
    if x1_x2 == 2:  # It could be a capture move
        if board[int((x1 + x2) / 2)][int((y1 + y2) / 2)].lower() != getOpponentColor(color):
            # Middle piece must be opponent
            return False

    return True

def canKingMoveToPosition(board, x1, y1, x2, y2, direction):
    # Check whether (x1,y1) can move to (x2,y2) in one move (plain or capture)

    if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x1 > 7 or y1 > 5 or x2 > 7 or y2 > 5:
        return False

    color = board[x1][y1]
    if color == ' ':
        return False
    if board[x2][y2] != ' ':
        return False
    x1_x2 = abs(x1 - x2)
    y1_y2 = abs(y1 - y2)
    #if x1_x2 != 1 and x1_x2 != 2:
       # return False
    if x1_x2 != y1_y2:
        return False
    #if color == 'o' and x2 > x1:  # o men cannot move down
        #return False
    #if color == 'x' and x2 < x1:  # x men cannot move up
        #return False
    if x1_x2 >= 2:  # It could be a capture move

        abs_dist = x1_x2

        while abs_dist >= 2:

            abs_dist = abs_dist - 1
            # - -
            if direction == "nw":
                if board[int(x1 - abs_dist)][int(y1 - abs_dist)].lower() != getOpponentColor(color):
                    return False

                count = 0
                r = x1_x2 - 1
                while r > 0:
                    if board[int(x1 - r)][int(y1 - r)].lower() != ' ':
                        count = count + 1
                    r = r - 1
                if count > 1:
                    return False
                return True
            # - +
            elif direction == "ne":
                if board[int(x1 - abs_dist)][int(y1 + abs_dist)].lower() != getOpponentColor(color):
                    return False

                count = 0
                r = x1_x2 - 1
                while r > 0:
                    if board[int(x1 - r)][int(y1 + r)].lower() != ' ':
                        count = count + 1
                    r = r - 1
                if count > 1:
                    return False
                return True

            # + -
            elif direction == "sw":
                if board[int(x1 + abs_dist)][int(y1 - abs_dist)].lower() != getOpponentColor(color):
                    return False

                count = 0
                r = x1_x2 - 1
                while r > 0:
                    if board[int(x1 + r)][int(y1 - r)].lower() != ' ':
                        count = count + 1
                    r = r - 1
                if count > 1:
                    return False
                return True

            # + +
            elif direction == "se":
                if board[int(x1 + abs_dist)][int(y1 + abs_dist)].lower() != getOpponentColor(color):
                    return False

                count = 0
                r = x1_x2 - 1
                while r > 0:
                    if board[int(x1 + r)][int(y1 + r)].lower() != ' ':
                        count = count + 1
                    r = r - 1
                if count > 1:
                    return False
                return True


    return True


def isLegalMove(board, move, color):
    # Check whether move (a list) is a legal move in the board for <color> piece
    if len(move) < 2:
        return False

    # Get the starting move position
    xy = serialToGrid(move[0])
    x1 = xy[0]
    y1 = xy[1]

    if board[x1][y1].lower() != color.lower():
        return False

    # See whether a capture is possible, if possible the player must capture
    isCaptureMove = isCapturePossible(board, color)

    # If not a capture move, there should be only 2 items in the move list
    if not isCaptureMove and len(move) != 2:
        return False

    # Temp board
    tempBoard = deepcopy(board)

    # Loop through 2nd to last items on the move list
    for i in range(1, len(move)):
        xy = serialToGrid(move[i])
        x2 = xy[0]
        y2 = xy[1]

        #King
        if tempBoard[x1][y1] == color.upper():
            direction = ""
            if x2 < x1 and y2 < y1:
                direction = "nw"
            elif x2 < x1 and y2 > y1:
                direction = "ne"
            elif x2 > x1 and y2 < y1:
                direction = "sw"
            elif x2 > x1 and y2 > y1:
                direction = "se"

            if not canKingMoveToPosition(tempBoard, x1, y1, x2, y2, direction):
                return False
        else:
            if not canMoveToPosition(tempBoard, x1, y1, x2, y2):
                return False

        # Perform the move
        if isCaptureMove != doMovePosition(tempBoard, x1, y1, x2, y2):
            return False

        # Preparing for next loop
        x1 = x2
        y1 = y2

    # Check whether the jump is complete
    # whether any more jump can be made from the last position
    if isCaptureMove:
        if isCapturePossibleFromPosition(tempBoard, x1, y1, color):
            return False

    return True


def isAnyMovePossible(board, color):
    # Returns whether any of the <color> pieces can make a valid move (plain or capture) at this time

    # Loop through all board positions
    for piece in range(1, 25):
        xy = serialToGrid(piece)
        x = xy[0]
        y = xy[1]

        # Check whether this board position is our color
        if board[x][y].upper() == color.upper():
            if canMoveToPosition(board, x, y, x - 1, y - 1):
                # Can move to top left
                return True
            if canMoveToPosition(board, x, y, x - 1, y + 1):
                # Can move to top right
                return True
            if canMoveToPosition(board, x, y, x + 1, y - 1):
                # Can move to bottom left
                return True
            if canMoveToPosition(board, x, y, x + 1, y + 1):
                # Can move to bottom right
                return True

    # If it can capture, it has moves
    if isCapturePossible(board, color):
        return True

    return False


def currentCountPieces(board):
    # Return number of <color> pieces (man or king) there are

    count_of_o = 0
    count_of_x = 0

    if countPieces(board, 'x') == 1 and countPieces(board, 'o') == 1:
        count_O, count_X = countKingPieces(board)
        if count_O + count_X == 2:
            return "Draw", count_O, count_X

    # Loop through all board positions
    for piece in range(1, 25):
        xy = serialToGrid(piece)
        x = xy[0]
        y = xy[1]

        # Check whether this board position is our color
        if board[x][y].upper() == 'o'.upper():
            count_of_o = count_of_o + 1
        elif board[x][y].upper() == 'x'.upper():
            count_of_x = count_of_x + 1

    if count_of_o == 0:
        return 'X', count_of_o, count_of_x
    elif count_of_x == 0:
        return 'O', count_of_o, count_of_x
    else:
        return None, count_of_o, count_of_x


def countPieces(board, color):
    # Return number of <color> pieces (man or king) there are

    count = 0

    # Loop through all board positions
    for piece in range(1, 25):
        xy = serialToGrid(piece)
        x = xy[0]
        y = xy[1]
        # Check whether this board position is our color
        if board[x][y].upper() == color.upper():
            count = count + 1

    return count


def countKingPieces(board):

    # Return number of <color> pieces (man or king) there are

    count_X = 0
    count_O = 0
    # Loop through all board positions
    for piece in range(1, 25):
        xy = serialToGrid(piece)
        x = xy[0]
        y = xy[1]

        # Check whether this board position is our color
        if board[x][y] == "X":
            count_X = count_X + 1
        elif board[x][y] == "O":
            count_O = count_O + 1

    return count_O, count_X

def countEdgePieces(board):

    count_o = 0
    count_x = 0
    # Loop through all board positions
    for piece in range(1, 25):
        xy = serialToGrid(piece)
        x = xy[0]
        y = xy[1]

        # Check whether this board position is our color
        if y == 0 or y == 5:
            if board[x][y].upper() == 'x'.upper():
                count_x = count_x + 1
            elif board[x][y].upper() == 'o'.upper():
                count_o = count_o + 1

    return count_o, count_x


def serialToGrid(serial):
    # Given a piece's serial 1-24 it will return the board grid position (0,0)~(7,5)
    return ((serial - 1) // 3, 2 * ((serial - 1) % 3) + 1  - ((((serial - 1) // 3) + 1) % 2))


def evaluate_actions_and_states(board, moves):
    """Returns list of available moves given current states and next states."""
    actions = []
    states = []
    for i in moves:
        actions.append(i)
        tempBoard = deepcopy(board)
        doMove(tempBoard, i)
        states.append(get_state(board, tempBoard))
    return states, actions


def get_state(old_board, board):

    winner, board_o, board_x = currentCountPieces(board)
    board_O, board_X = countKingPieces(board)
    center_o, center_x = center_of_mass(board)
    edge_o, edge_x = countEdgePieces(board)

    winner, old_board_o, old_board_x = currentCountPieces(old_board)
    old_board_O, old_board_X = countKingPieces(old_board)
    old_center_o, old_center_x = center_of_mass(old_board)
    old_edge_o, old_edge_x = countEdgePieces(old_board)
    state =  old_board_o, old_board_x, old_board_O, old_board_X, old_edge_o, old_center_o, old_center_x, board_o, board_x, board_O, board_X, edge_o, center_o, center_x
    state = " ".join(map(str,state))
    return ''.join(state)


def newBoard():
    # Create a new board, 2D array of characters
    # 'x' for man, 'o' for man
    # 'X' for king, 'O' for king
    # ' ' for empty

    board = []
    for i in range(8):
        board.append([' '] * 6)

    for i in range(1, 10):
        xy = serialToGrid(i)
        x = xy[0]
        y = xy[1]
        #print("x:" + str(x) + "\t" + "y:" + str(y))
        board[x][y] = 'x'

    for i in range(16, 25):
        xy = serialToGrid(i)
        x = xy[0]
        y = xy[1]
        #print("x:" + str(x) + "\t" + "y:" + str(y))
        board[x][y] = 'o'

    return board

def center_of_mass(board):

    array_of_o = np.array(board)
    array_of_x = np.array(board)

    array_of_o[array_of_o == 'o'] = 1
    array_of_o[array_of_o == 'O'] = 1
    array_of_o[array_of_o == 'x'] = 0
    array_of_o[array_of_o == 'X'] = 0
    array_of_o[array_of_o == ' '] = 0

    array_of_x[array_of_x == 'x'] = 1
    array_of_x[array_of_x == 'X'] = 1
    array_of_x[array_of_x == 'o'] = 0
    array_of_x[array_of_x == 'O'] = 0
    array_of_x[array_of_x == ' '] = 0

    array_of_o = array_of_o.astype(int)
    array_of_x = array_of_x.astype(int)

    center_o = ndimage.measurements.center_of_mass(array_of_o)
    center_x = ndimage.measurements.center_of_mass(array_of_x)

    if math.isnan(center_x[0]):
        center_x = (0, 1)

    return np.int(center_o[0]), np.int(center_x[0])

def printBoard(board):
    # Print a board
    numberedBoard = [
		['1 ', '  ', '2 ', '  ', '3 ', '  '],
		['  ', '4 ', '  ', '5 ', '  ', '6 '],
		['7 ', '  ', '8 ', '  ', '9 ', '  '],
		['  ', '10', '  ', '11', '  ', '12'],
		['13', '  ', '14', '  ', '15', '  '],
		['  ', '16', '  ', '17', '  ', '18'],
		['19', '  ', '20', '  ', '21', '  '],
		['  ', '22', '  ', '23', '  ', '24']
	]

    columns = ["A", "B", "C", "D", "E", "F"]
    rows = ["1", "2", "3", "4", "5", "6", "7", "8"]
    print('    ', '   '.join(colored(column, 'blue') for column in columns), ' ')
    print(' ' * 2, '-' * 25, '\t', '-' * 30)
    for i in range(0, 8):
        print(colored(rows[i], 'blue'), ' ' '|', ' | '.join(printColor(symbol) for symbol in board[i]), '|', '\t|', ' | '.join(numberedBoard[i]), '|')
        print(' ' * 2, '-' * 25, '\t', '-' * 30)

def printColor(item):
    if item.isupper():
        return colored(item, 'blue')
    return item

def playGame(p1, p2, verbose, mode):
    # Takes as input two functions p1 and p2 (each of which
    # calculates a next move given a board and player color),
    # and returns a tuple containing
    # the final board,
    # pieces left for red,
    # pieces left for white,
    # and status message "Drawn"/"Won"/"Timeout"/"Bad Move"
    board = newBoard()
    printBoard(board)
    print
    if p1_str == "Player1":
        currentColor = 'x'
        nextColor = 'o'
    else:
        currentColor = 'o'
        nextColor = 'x'

    while isAnyMovePossible(board, currentColor) or (countPieces(board, 'x') >= 1 and countPieces(board, 'o') >= 1):
        tempBoard = deepcopy(board)
        nextMove = p1(tempBoard, currentColor, mode)

        if isLegalMove(board, nextMove, currentColor):
            doMove(board, nextMove)

        #else:
            #if currentColor == "x":
                #return (board, -1, 1, "Bad Move: %s" % str(nextMove))
            #else:
                #return (board, 1, -1, "Bad Move: %s" % str(nextMove))

        (p1, p2) = (p2, p1)
        (currentColor, nextColor) = (nextColor, currentColor)

        if verbose:
            printBoard(board)
            print("Pieces remaining:", colored(currentColor, 'yellow'), "=", countPieces(board, currentColor), " ", colored(nextColor, 'yellow'), "=", countPieces(board, nextColor))
            print("---------------------------------- End of", colored(nextColor, 'yellow') + "\'s", "turn", "----------------------------------","\n")
            print("\n", "\n")

        if countPieces(board, 'x') == 1 and countPieces(board, 'o') == 1:
            count_O, count_X = countKingPieces(board)
            if count_O + count_X == 2:
                return (board, countPieces(board, 'x'), countPieces(board, 'o'), "Drawn")

    return (board, countPieces(board, 'x'), countPieces(board, 'o'), "Won")


if __name__ == "__main__":
    while True:
        beginning = input("Who is going to start?	\"1\" for Player1 \"2\" for Player2")
        mode = input("Is it \"train\" or \"game\"")
        exec("from Player" + str(beginning) + " import nextMove")
        p1 = nextMove
        p1_str = "Player" + str(beginning)
        exec("from Player" + str(int(beginning)%2 + 1) + " import nextMove")
        p2 = nextMove
        p2_str = "Player" + str(int(beginning)%2 + 1)

        if mode == "train":

            i = 0

            while i < 100:
                if i % 10 == 0:
                    print("-------------- TRAINING EPISODE", i, "--------------")
                result = playGame(p1, p2, True, mode)

                printBoard(result[0])

                if result[3] == "Drawn":
                    if result[1] > result[2]:
                        print("Ran Out Of Moves :: %s Wins %s Loses (%d to %d)" % (p1_str, p2_str, result[1], result[2]))
                    elif result[1] < result[2]:
                        print("Ran Out Of Moves :: %s Wins %s Loses (%d to %d)" % (p2_str, p1_str, result[2], result[1]))
                    else:
                        print("Ran Out Of Moves :: TIE %s, %s, (%d to %d)" % (p1_str, p2_str, result[1], result[2]))
                elif result[3] == "Won":
                    if result[1] > result[2]:
                        print("%s Wins %s Loses (%d to %d)" % (p1_str, p2_str, result[1], result[2]))
                    elif result[1] < result[2]:
                        print("%s Wins %s Loses (%d to %d)" % (p2_str, p1_str, result[2], result[1]))

                from Player2 import reset_values
                reset_values()

                i = i + 1

            from Player2 import save_values
            save_values()

        else:

            result = playGame(p1, p2, True, mode)

            printBoard(result[0])

            if result[3] == "Drawn":
                if result[1] > result[2]:
                    print("Ran Out Of Moves :: %s Wins %s Loses (%d to %d)" % (p1_str, p2_str, result[1], result[2]))
                elif result[1] < result[2]:
                    print("Ran Out Of Moves :: %s Wins %s Loses (%d to %d)" % (p2_str, p1_str, result[2], result[1]))
                else:
                    print("Ran Out Of Moves :: TIE %s, %s, (%d to %d)" % (p1_str, p2_str, result[1], result[2]))
            elif result[3] == "Won":
                if result[1] > result[2]:
                    print("%s Wins %s Loses (%d to %d)" % (p1_str, p2_str, result[1], result[2]))
                elif result[1] < result[2]:
                    print("%s Wins %s Loses (%d to %d)" % (p2_str, p1_str, result[2], result[1]))
