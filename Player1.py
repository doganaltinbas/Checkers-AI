import random
import gamePlay
import time
from getAllPossibleMoves import getAllPossibleMoves
from termcolor import colored

def nextMove(board, color):

	moved = False
	while not moved:
		print("---------------------------------- ", colored(color, 'yellow')+"\'s", "turn", "----------------------------------------","\n")
		possibleMoves = getAllPossibleMoves(board, color)
		print(colored('Possible moves:', 'yellow', attrs=['bold', 'blink']), possibleMoves)
		#moveStr = input("Please enter your move(" + color + "): ")

		if len(possibleMoves) == 0:
			print("No possible moves. Switching players...")
			return []

		randomMove = random.choice(possibleMoves)
		randomMove = [str(i) for i in randomMove]
		randomMove = ','.join(randomMove)
		print("random move(" + color + "): " + randomMove)
		my_move_list = randomMove.replace(' ', '').split(',')
		my_move_list = list(map(int, my_move_list))
		time.sleep(0.2)
		if gamePlay.isLegalMove(board, my_move_list, color):
			moved = True
			return my_move_list
		else:
			print("Illegal move", str(my_move_list))
		
