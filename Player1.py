import random
import gamePlay
from getAllPossibleMoves import getAllPossibleMoves


def nextMove(board, color):

	moved = False
	while moved == False:

		possibleMoves = getAllPossibleMoves(board, color)
		print ('Possible moves:', possibleMoves)
		moveStr = input("Please enter your move(" + color + "): ")

		my_move_list = moveStr.replace(' ', '').split(',')
		my_move_list = list(map(int, my_move_list))

		if gamePlay.isLegalMove(board, my_move_list, color):
			moved = True			
			return my_move_list
		else:
			print ("Illegal move", str(my_move_list))
		
