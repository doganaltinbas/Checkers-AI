from copy import deepcopy

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


def isCapturePossibleFromPosition(board, x, y):
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
            if isCapturePossibleFromPosition(board, x, y):
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

    if abs(x1 - x2) == 2:  # It's a capture move
        board[int((x1 + x2) / 2)][int((y1 + y2) / 2)] = ' '
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
        if isCapturePossibleFromPosition(tempBoard, x1, y1):
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

    count = 0

    # Loop through all board positions
    for piece in range(1, 25):
        xy = serialToGrid(piece)
        x = xy[0]
        y = xy[1]

        # Check whether this board position is our color
        if board[x][y] == "X" or board[x][y] == "O":
            count = count + 1
    return count

def serialToGrid(serial):
    # Given a piece's serial 1-24 it will return the board grid position (0,0)~(7,5)
    return ((serial - 1) // 3, 2 * ((serial - 1) % 3) + 1  - ((((serial - 1) // 3) + 1) % 2))


def newBoard():
    # Create a new board, 2D array of characters
    # 'x' for red man, 'o' for white man
    # 'X' for red king, 'O' for white king
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
    print('    ', '   '.join(columns), ' ')
    print(' ' * 2, '-' * 25, '\t', '-' * 30)
    for i in range(0, 8):
        print(rows[i], ' ' '|', ' | '.join(board[i]), '|', '\t|', ' | '.join(numberedBoard[i]), '|')
        print(' ' * 2, '-' * 25, '\t', '-' * 30)


def playGame(p1, p2, verbose):
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
    currentColor = 'x'
    nextColor = 'o'

    while isAnyMovePossible(board, currentColor) or (countPieces(board, 'x') >= 1 and countPieces(board, 'o') >= 1):
        tempBoard = deepcopy(board)
        nextMove = p1(tempBoard, currentColor)

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
            print("Pieces remaining:", currentColor, "=", countPieces(board, currentColor), " ", nextColor, "=", countPieces(board, nextColor))
            print()

        if countPieces(board, 'x') == 1 and countPieces(board, 'o') == 1:
            if countKingPieces(board) == 2:
                return (board, countPieces(board, 'x'), countPieces(board, 'o'), "Drawn")

    return (board, countPieces(board, 'x'), countPieces(board, 'o'), "Won")


if __name__ == "__main__":
    beginning = input("Who is going to start?	\"1\" for Player1 \"2\" for Player2")

    exec("from Player1 import nextMove")
    p1 = nextMove
    p1_str = "Player" + str(beginning)
    #exec("from Player" + str(int(beginning) + (int(beginning) % 2)) + " import nextMove")
    p2 = nextMove
    p2_str = "Player" + str(int(beginning)%2 + 1)
    result = playGame(p1, p2, True)

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

