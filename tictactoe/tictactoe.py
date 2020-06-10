"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    X_count = 0
    O_count = 0
    for row in board:
        for i in row:
            if i == 'X':
                X_count += 1
            elif i == 'O':
                O_count +=1
    #print("X_count is: "+str(X_count))
    #print("O_count is: "+str(O_count))

    if O_count >= X_count:
        return X
    else:
        return O


def actions(board):
    #Check which actions are available

    actions = set()

    for row in range(0,3):
        for column in range(0,3):
            if board[row][column] == EMPTY:
                actions.add((row,column))

    return actions



def result(board, action):

    #first we check who's move it is
    value = player(board)
    #making a deepcopy
    new_board = copy.deepcopy(board)
    potential_actions = actions(board)
    #print(action)
    #print(potential_actions)
    if action not in potential_actions:
        raise Exception("That was not a valid move!")

    else:
        new_board[action[0]][action[1]]= value

    return new_board


def winner(board):

    #Checks the rows
    for row in range(0,3):
        if board[row] == [X,X,X]:
            return X
        elif board[row] == [O,O,O]:
            return O

    #checks the columns
    for col in range(0,3):
        if board[0][col] == X and board[1][col] == X and board[2][col] == X:
            return X
        elif board[0][col] == O and board[1][col] == O and board[2][col] == O:
            return O

    #checks the diagonals
    if board[0][0] == X and board[1][1] == X and board [2][2] == X:
        return X

    elif board[0][0] == O and board[1][1] == O and board [2][2] == O:
        return O

    elif board[0][2] == X and board[1][1] == X and board [2][0] == X:
        return X

    elif board[0][2] == O and board[1][1] == O and board [2][0] == O:
        return O

    return None


def terminal(board):
    terminated = True
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == EMPTY:
                terminated = False

    if winner(board) == X or winner(board) == O:
        terminated = True

    return terminated


def utility(board):

    value = winner(board)

    if value == X:
        return 1
    elif value == O:
        return -1

    return 0


def minimax(board):
    #checks if game is over
    if terminal(board):
        return None

    #checks if it's X or O's turn
    value = player(board)
    if value == X:
        action = max_move(board)

    elif value == O:
        action = min_move(board)

    else:
        raise Exception("Incorrect value submitted")

    return action[1]

def max_move(board):
    #make it return an array with values, v and action
    v = -100
    #check if there are any actions left

    #check if its terminal
    if terminal(board):
        arr = utility(board)
        array = [arr,1]

        return array

    for action in actions(board):
        w = min_move(result(board,action))
        w = w[0]
        new_v = max(v, w)
        if new_v > v:
            v = new_v
            optimal_action = action

    return [v,optimal_action]

def min_move(board):
    #make it return an array with values v and action
    v = 100

    #check if its terminal
    if terminal(board):
        arr = utility(board)
        array = [arr,1]

        return array

    for action in actions(board):
        w = max_move(result(board,action))
        w = w[0]
        new_v = min(v,w)
        if new_v < v:
            v = new_v
            optimal_action = action

    return [v,optimal_action]
