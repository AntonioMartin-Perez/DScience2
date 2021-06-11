"""
Tic Tac Toe Player
"""

import math

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
    """
    Returns player who has the next turn on a board.

    count x and os

    """
    x = 0
    o = 0

    for i in range(3):
        for j in range(3):
            if(board[i][j] == X):
                x += 1
            elif(board[i][j] == O):
                o += 1
    if(x == o):
        return X
    else:
        return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set = []
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                set.append((i,j))
    return set
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    new_board = board
    (i,j) = action
    new_board[i][j] = player(board)
    return new_board
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if(board[0][0] == X and board[0][1] == X and board[0][2] == X):
        return X
    if(board[1][0] == X and board[1][1] == X and board[1][2] == X):
        return X
    if(board[2][0] == X and board[2][1] == X and board[2][2] == X):
        return X
    if(board[0][0] == X and board[1][0] == X and board[2][0] == X):
        return X
    if(board[0][1] == X and board[1][1] == X and board[2][1] == X):
        return X
    if(board[0][2] == X and board[1][2] == X and board[2][2] == X):
        return X
    if(board[0][0] == X and board[1][1] == X and board[2][2] == X):
        return X
    if(board[2][0] == X and board[1][1] == X and board[0][2] == X):
        return X

    if(board[0][0] == O and board[0][1] == O and board[0][2] == O):
        return O
    if(board[1][0] == O and board[1][1] == O and board[1][2] == O):
        return O
    if(board[2][0] == O and board[2][1] == O and board[2][2] == O):
        return O
    if(board[0][0] == O and board[1][0] == O and board[2][0] == O):
        return O
    if(board[0][1] == O and board[1][1] == O and board[2][1] == O):
        return O
    if(board[0][2] == O and board[1][2] == O and board[2][2] == O):
        return O
    if(board[0][0] == O and board[1][1] == O and board[2][2] == O):
        return O
    if(board[2][0] == O and board[1][1] == O and board[0][2] == O):
        return O
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    return len(actions(board)) == 0
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

    raise NotImplementedError

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    bestAction = None
    bestScore = -math.inf

    for action in actions(board):
    	if max_value(result(board, action)) > bestScore:
            bestAction = action
            bestScore = max_value(result(board, action))
    return bestAction
    raise NotImplementedError
