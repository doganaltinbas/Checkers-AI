import gamePlay
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves
import numpy as np
import gamePlay
from termcolor import colored
import sys
import json


qtable = dict()
learning_rate = 5e-1
discount = 9e-1
epsilon = 5e-1
episode_reward = 0
total_reward = 0
cumulative_reward = []
memory = []
history = []


def qvalue(state):
    """Retrieve value from qtable or initialize if not found."""
    if state not in qtable:
        # Initialize Q-value at 0
        qtable[state] = 0.0
    return qtable[state]


def argmax(values):
    """Returns index of max value."""
    vmax = np.max(values)
    max_indices = []
    for i, v in enumerate(values):
        if v == vmax:
            max_indices.append(i)
    return np.random.choice(max_indices)

def step(board, color, verbose= True):
    """Agent makes one step.

	- Deciding optimal or random action following e-greedy strategy given current state
	- Taking selected action and observing next state
	- Calculating immediate reward of taking action, current state, and next state
	- Updating q table values using GD with derivative of MSE of Q-value
	- Returns game status
	"""
    old_board = deepcopy(board)
    state, action = next_move(board, color)
    temp_board = deepcopy(board)
    gamePlay.doMove(temp_board, action)
    reward_value, winner = reward(old_board, temp_board)
    update(reward_value, winner, state, board, color)
    if verbose:
        print("=========")
        print(colored("Selected Move:", 'yellow'), action)
        print(colored("Winner:", 'yellow'), winner)
        print(colored("State:", 'yellow'), state)
        print(colored('Q value:', 'yellow'), '{}'.format(qvalue(state)))
        print(colored("Reward value:", 'yellow'), reward_value)
    return winner, reward_value, action


def next_move(board, color):
    """Selects next move in MDP following e-greedy strategy."""
    moves = getAllPossibleMoves(board, color)
    print(colored('Possible moves:', 'yellow', attrs=['bold']), moves)
    states, actions = gamePlay.evaluate_actions_and_states(board, moves)
    for i, val in enumerate(states):
        print("state:", val, "\naction:", actions[i])
    i = optimal_next(states)
    if np.random.random_sample() < epsilon:
        # Explore
        i = np.random.randint(0, len(states))
    return states[i], actions[i]


def optimal_next(states):
    """Selects optimal next move.
	Input
	- states list of possible next states
	Output
	- index of next state that produces maximum value
	"""
    values = [qvalue(s) for s in states]
    # Exploit
    return argmax(values)


def reward(old_board, board):
        """Calculates reward for different end game conditions.
        - win is 1.0
        - loss is -1.0
        - draw and unfinished is calculate by:
         Format of returned data:
         (own_pieces, opp_pieces, own_kings, opp_kings, own_edges, own_vert_center_mass, opp_vert_center_mass)
        """
        winner, count_o, count_x = gamePlay.currentCountPieces(board)

        if winner == 'O':
            return 9.0, winner
        elif winner == 'X':
            return -9.0, winner
        else:
            #calculate old_board and board piece counts

            winner, board_o, board_x = gamePlay.currentCountPieces(board)
            board_O, board_X = gamePlay.countKingPieces(board)

            winner, old_board_o, old_board_x = gamePlay.currentCountPieces(old_board)
            old_board_O, old_board_X = gamePlay.countKingPieces(old_board)

            calc = board_o - old_board_o + 2*(board_O - old_board_O) - (board_x - old_board_x) - 2*(board_X - old_board_X)
            return calc, winner

def update(reward, winner, state, board, color):
    """Updates q-value.
	Update uses recorded observations of performing a
	certain action in a certain state and continuing optimally from there."""
    # Finding estimated future value by finding max(Q(s', a'))
    # If terminal condition is reached, future reward is 0
    future_val = 0
    if not winner:
        moves = getAllPossibleMoves(board, color, False)
        future_states, _ = gamePlay.evaluate_actions_and_states(board, moves)
        i = optimal_next(future_states)
        future_val = qvalue(future_states[i])
    # Q-value update
    qtable[state] = ((1 - learning_rate) * qvalue(state)) + (learning_rate * (reward + discount * future_val))

def train(board, color):
    """Trains by playing
	Each episode is a full game"""
    moves = getAllPossibleMoves(board, color, False)
    if len(moves) == 0:
        print("No Possible move for AI. Switching players...")
        return []
    winner, reward, action = step(board, color)
    global episode_reward
    #print("episode_reward",episode_reward)
    episode_reward += reward
    global total_reward
    #print("total_reward",total_reward)
    total_reward += episode_reward
    global cumulative_reward
    #print("cumulative_reward", cumulative_reward)
    cumulative_reward.append(total_reward)
    global memory
    #print(memory)
    memory.append(sys.getsizeof(qtable) / 1024)
    return action

def reset_values():
    global episode_reward
    print("resetted",episode_reward)
    episode_reward = 0


def get_history():
    global history
    history.append(100)
    history.append(cumulative_reward)
    history.append(memory)
    return history

def save_values(path='data/qtable.json'):
    """Save Q values to json."""
    with open(path, 'w') as out:
        json.dump(qtable, out)

def nextMove(board, color, mode):
    print("---------------------------------- ", colored(color, 'yellow') + "\'s", "turn","----------------------------------------", "\n")
    if mode == "train":
        return train(board, color)
    else:
        moves = getAllPossibleMoves(board, color)
        print(colored('Possible moves:', 'yellow', attrs=['bold']), moves)
        states, actions = gamePlay.evaluate_actions_and_states(board, moves)
        for i, val in enumerate(states):
            print("state:", val, "\naction:", actions[i])
        i = optimal_next(states)
        print(colored("AI selected move:", 'yellow'), actions[i])
        return actions[i]
