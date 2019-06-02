import gamePlay
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves
import numpy as np
import gamePlay
from termcolor import colored

'''
The code makes use of recursion to implement minimax with alpha beta pruning.
'''

qtable = dict()
player = 'X'
learning_rate = 5e-1
discount = 9e-1
epsilon = 5e-1


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

def argmin(values):
    """Returns index of min value."""
    vmin = np.min(values)
    min_indices = []
    for i, v in enumerate(values):
        if v == vmin:
            min_indices.append(i)
    return np.random.choice(min_indices)

def step(verbose=True):
    """Agent makes one step.

	- Deciding optimal or random action following e-greedy strategy given current state
	- Taking selected action and observing next state
	- Calculating immediate reward of taking action, current state, and next state
	- Updating q table values using GD with derivative of MSE of Q-value
	- Returns game status
	"""
    old_board = [val for val in game.board]
    state, action = next_move()
    winner = game.make_move(action)
    reward = reward(winner)
    update(reward, winner, state)
    if verbose:
        print("=========")
        print(old_board)
        print(action)
        print(winner)
        print(state)
        print('Q value: {}'.format(qvalue(state)))
        game.print_board()
        print(reward)
    return (winner, reward)


def next_move(board, color):
    """Selects next move in MDP following e-greedy strategy."""
    states, actions = game.get_open_moves()
    # Exploit
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
    if game.player == player:
        # Optimal move is max
        return argmax(values)
    else:
        # Optimal move is min
        return argmin(values)

def reward(winner):
        """Calculates reward for different end game conditions.
        - win is 1.0
        - loss is -1.0
        - draw and unfinished is 0.0
        """
        opponent = 'O' if player == 'X' else 'X'
        if (winner == player):
            return 1.0
        elif (winner == opponent):
            return -1.0
        else:
            return 0

def update(reward, winner, state):
    """Updates q-value.

	Update uses recorded observations of performing a
	certain action in a certain state and continuing optimally from there."""
    # Finding estimated future value by finding max(Q(s', a'))
    # If terminal condition is reached, future reward is 0
    future_val = 0
    if not winner:
        future_states, _ = game.get_open_moves()
        i = optimal_next(future_states)
        future_val = qvalue(future_states[i])
    # Q-value update
    qtable[state] = ((1 - learning_rate) * qvalue(state)) + (learning_rate * (reward + discount * future_val))


def train(episodes, history=[]):
    """Trains by playing against
	Each episode is a full game"""
    x = range(episodes)
    cumulative_reward = []
    memory = []

    total_reward = 0.0
    for i in range(episodes):
        episode_reward = 0.0
        game_active = True
        # Rest of game follows strategy
        while (game_active):
            winner, reward = step()
            episode_reward += reward
            if winner:
                game_active = False
                game.reset()
        total_reward += episode_reward
        cumulative_reward.append(total_reward)
        global qtable
        memory.append(sys.getsizeof(qtable) / 1024)
        # Record total reward agent gains as training progresses
        if (i % (episodes / 10) == 0) and (i >= (episodes / 10)):
            print('.')
    history.append(x)
    history.append(cumulative_reward)
    history.append(memory)
    return history


def stats():
    """Agent plays optimally against self with no exploration.
	Records win/loss/draw distribution."""
    x_wins = 0
    o_wins = 0
    draws = 0
    episodes = 10000
    for i in range(episodes):
        game_active = True
        while (game_active):
            states, actions = game.get_open_moves()
            i = optimal_next(states)
            winner = game.make_move(actions[i])
            if winner:
                if (winner == 'X'):
                    x_wins += 1
                elif (winner == 'O'):
                    o_wins += 1
                else:
                    draws += 1
                game_active = False
                game.reset()
    print('    X: {} Draw: {} O: {}'.format((x_wins * 1.0) / episodes,
                                            (draws * 1.0) / episodes,
                                            (o_wins * 1.0) / episodes))


def save_values(path='data/qtable.json'):
    """Save Q values to json."""
    with open(path, 'w') as out:
        json.dump(qtable, out)


def demo(first=True):
    """Demo so users can play against trained agent."""
    game.print_instructions()
    # Agent goes first
    game_active = True
    while game_active:
        winner = None
        if first:
            states, actions = game.get_open_moves()
            i = optimal_next(states)
            winner = game.make_move(actions[i])
            game.print_board()
            first = not first
        elif not first:
            print('Select move:')
            p = game.read_input()
            if game.is_valid_move(p):
                winner = game.make_move(p)
                game.print_board()
                first = not first
            else:
                print('Invalid move.')
        if winner:
            print('Winner: {}'.format(winner))
            game_active = False
    game.reset()

def nextMove(board, color):
    print("---------------------------------- ", colored(color, 'yellow') + "\'s", "turn","----------------------------------------", "\n")
    moves = getAllPossibleMoves(board, color)
    print(colored('Possible moves:', 'yellow', attrs=['bold']), moves)
    states, actions = gamePlay.evaluate_actions_and_states(board, moves)
    for i, val in enumerate(states):
        print("state:", val,"\naction:", actions[i])
    opponentColor = gamePlay.getOpponentColor(color)
    depth = 5
    best = None
    alpha = None
    beta = float("inf")
    for move in moves: # this is the max turn(1st level of minimax), so next should be min's turn
        newBoard = deepcopy(board)
        gamePlay.doMove(newBoard,move)
        #Beta is always inf here as there is no parent MIN node. So no need to check if we can prune or not.
        moveVal = evaluation(newBoard, color, depth, 'min', opponentColor, alpha, beta)
        if best == None or moveVal > best:
            bestMove = move
            best = moveVal
        if best > alpha:
            alpha = best
    return bestMove