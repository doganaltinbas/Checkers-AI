import gamePlay
from copy import deepcopy
from termcolor import colored

def gridToSerial(x, y):
	# Returns the serial 1~24 of cell given the grid position(0,0)~(7,5)
	
	return 3*x+y//2+1


def getAllJumpMovesAtPosition(board, x, y, color):
	# Get all jump moves of position board(x,y)

	moves = []
	serial = gridToSerial(x, y)
	for i in [-2, 2]:
		for j in [-2, 2]:
			# Check all four directions
			if gamePlay.canMoveToPosition(board, x, y, x + i, y + j):
				tempBoard = deepcopy(board)
				gamePlay.doMovePosition(tempBoard, x, y, x + i, y + j)
				#if tempBoard[x + i][y + j] == color.upper():
					#print("it is upped")
				childJumpMoves = getAllJumpMovesAtPosition(tempBoard, x + i, y + j, color) if tempBoard[x + i][y + j] != color.upper() else getAllKingJumpMovesAtPosition(
					tempBoard, x + i, y + j)
				if len(childJumpMoves) == 0:
					moves.append([serial, gridToSerial(x + i, y + j)])
				else:
					for m in childJumpMoves:
						l = [serial]
						l.extend(m)
						moves.append(l)
	return moves


def getAllKingJumpMovesAtPosition(board, x, y):
	# Get all jump moves of position board(x,y)

	moves = []
	directions = ["nw", "ne", "sw", "se"]
	serial = gridToSerial(x, y)
	# king için 5 ten geriye while yapıp for loopa -i,i yapabiliriz.
	i = 5
	while (i > 1):
		k = i
		iter = 0
		for i in [-i, i]:
			for j in [-k, k]:
				# Check all four directions
				if gamePlay.canKingMoveToPosition(board, x, y, x + i, y + j, directions[iter]):
					tempBoard = deepcopy(board)
					gamePlay.doMovePosition(tempBoard, x, y, x + i, y + j)
					childJumpMoves = getAllKingJumpMovesAtPosition(tempBoard, x + i, y + j)
					if len(childJumpMoves) == 0:
						moves.append([serial, gridToSerial(x + i, y + j)])
					else:
						for m in childJumpMoves:
							l = [serial]
							l.extend(m)
							moves.append(l)
				iter = iter + 1
		i = i - 1
	return moves
	
def getAllPossibleMovesAtPosition(board, x, y, color):
	# Returns a tuple 
	# 1) list of all possible moves of the piece board[x][y]
	# 2) True/False, whether the moves are capture moves or not
	
	moves = []
	isCapture = False
	l = []
	# Look for jumps
	if board[x][y] == color.upper():
		l = getAllKingJumpMovesAtPosition(board, x, y)
		print(colored(board[x][y], 'blue'), "at", gridToSerial(x, y), colored("King", 'blue'), colored("Possible Jump Moves:", 'red'), l)
		for m in l:
			moves.append(m)
	else:
		l = getAllJumpMovesAtPosition(board, x, y, color)
		print(board[x][y], "at", gridToSerial(x, y), colored("Possible Jump Moves:", 'red'), l)
		for m in l:
			moves.append(m)

	if len(moves) == 0: # No jump moves available

		# Look for plain moves
		serial = gridToSerial(x,y)
		
		if gamePlay.canMoveToPosition(board, x, y, x-1, y-1):
			moves.append([serial,gridToSerial(x-1,y-1)])
		if gamePlay.canMoveToPosition(board, x, y, x-1, y+1):
			moves.append([serial,gridToSerial(x-1,y+1)])
		if gamePlay.canMoveToPosition(board, x, y, x+1, y-1):
			moves.append([serial,gridToSerial(x+1,y-1)])
		if gamePlay.canMoveToPosition(board, x, y, x+1, y+1):
			moves.append([serial,gridToSerial(x+1,y+1)])

		print(board[x][y], "at", gridToSerial(x, y), "Possible Regular Moves:", moves)

	else:
		isCapture = True
		
	return moves, isCapture
	
	
def getAllPossibleMoves(board, color):
	# Get a list of all possible moves of <color>
	
	moves = []
	jumpMoves = []
	# Get if capture is possible for current player
	isCapturePossible = gamePlay.isCapturePossible(board, color)
	
	# Loop through all board positions
	for piece in range(1, 25):
		xy = gamePlay.serialToGrid(piece)
		x = xy[0]
		y = xy[1]
		
		# Check whether this board position is our color
		if board[x][y].upper() == color.upper():

			l, isCapture = getAllPossibleMovesAtPosition(board, x, y, color)

			#if capture is possible, only capture moves should be appended.
			if isCapturePossible == isCapture:
				if isCapture:
					for m in l:
						jumpMoves.append(m)
					le = max(len(x) for x in jumpMoves)  # find out the max length
					jumpMoves = [x for x in jumpMoves if len(x) == le]  # now filter list based on that max length
					print(board[x][y], "at", gridToSerial(x, y), colored("Selected max Jump(s):", 'yellow', attrs=['bold']), jumpMoves)
					continue

				for m in l:
					moves.append(m)

	return moves if len(jumpMoves) == 0 else jumpMoves