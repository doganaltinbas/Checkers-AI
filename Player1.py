import random
import gamePlay
import time
from getAllPossibleMoves import getAllPossibleMoves
from termcolor import colored

def nextMove(board, color, mode):

	while True:
		print("---------------------------------- ", colored(color, 'yellow')+"\'s", "turn", "----------------------------------------","\n")
		possibleMoves = getAllPossibleMoves(board, color)
		print(colored('Possible moves:', 'yellow', attrs=['bold', 'blink']), possibleMoves)

		if len(possibleMoves) == 0:
			print("No possible moves. Switching players...")
			return []

		#train mode
		if mode == "train":
			randomMove = random.choice(possibleMoves)
			randomMove = [str(i) for i in randomMove]
			randomMove = ','.join(randomMove)
			print("random move(" + color + "): " + randomMove)
			my_move_list = randomMove.replace(' ', '').split(',')
			my_move_list = list(map(int, my_move_list))

			if gamePlay.isLegalMove(board, my_move_list, color):
				return my_move_list
			else:
				print("Illegal move", str(my_move_list))

		#game mode
		else:
			moveStr = input("Please enter your move(" + color + "): ")
			print("Selected move(" + color + "): " + moveStr)
			my_move_list = moveStr.replace(' ', '').split(',')
			my_move_list = list(map(int, my_move_list))

			if gamePlay.isLegalMove(board, my_move_list, color):
				return my_move_list
			else:
				print("Illegal move", str(my_move_list))



