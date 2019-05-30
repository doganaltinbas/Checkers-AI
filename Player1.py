import random
import gamePlay
import time
from getAllPossibleMoves import getAllPossibleMoves
import os

def nextMove(board, color):

	moved = False
	while moved == False:
		possibleMoves = getAllPossibleMoves(board, color)
		print ('Possible moves:', possibleMoves)
		#moveStr = input("Please enter your move(" + color + "): ")
		randomMove = random.choice(possibleMoves)
		randomMove = [str(i) for i in randomMove]
		randomMove = ','.join(randomMove)
		print("random move(" + color + "): " + randomMove)
		my_move_list = randomMove.replace(' ', '').split(',')
		my_move_list = list(map(int, my_move_list))
		time.sleep(0.5)
		if gamePlay.isLegalMove(board, my_move_list, color):
			moved = True			
			return my_move_list
		else:
			print ("Illegal move", str(my_move_list))
		
