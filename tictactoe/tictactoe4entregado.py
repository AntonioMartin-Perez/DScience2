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
    """
    movesMade = 0
    for row in board:
        movesMade += row.count(X)
        movesMade += row.count(O)

    if movesMade % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    i = -1
    actions = set()

    for row in board:
        i += 1
        j = 0
        for element in row:
            if element is EMPTY:
                actions.add( (i,j) )
            j +=1
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    turn            =       player(board)
    i,j             =       action
    newboard        =       [i.copy() for i in board]
    newboard[i][j]  =       turn
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # rows and columns
    for n in range(0,3):
        if board[n][:] == [X,X,X] or [element[n] for element in board] == [X,X,X]:
            return X
        elif board[n][:] == [O,O,O] or [element[n] for element in board] == [O,O,O]:
            return O
    # diagonals
    if [board[0][0]] + [board[1][1]] + [board[2][2]] == [X,X,X] or [board[-1][0]] + [board[-2][1]] + [board[-3][2]] == [X,X,X]:
        return X
    if [board[0][0]] + [board[1][1]] + [board[2][2]] == [O,O,O] or [board[-1][0]] + [board[-2][1]] + [board[-3][2]] == [O,O,O]:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len( actions(board) ) == 0 or winner(board) is not None:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def maxValue(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(  v,minValue( result(board,action) )  )
    return v - 0.001

def minValue(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(  v,maxValue( result(board,action) )  )
    return v + 0.001

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if board == initial_state():
        return (1,1)

    bestAction = None

    if player(board) == X:
        bestScore = - math.inf   
        for action in actions(board):
            value = maxValue( result(board, action) )
            if value > bestScore:
                bestAction = action
                bestScore = value
    else:
        bestScore = math.inf 
        for action in actions(board):
            value = minValue( result(board, action) )
            if value < bestScore:
                bestAction = action
                bestScore = value

    return bestAction


################################################## Pruebas ###############################################################
ini = initial_state()
board1 = [[None, X, None], [O, None, X], [None, None, None]]
board2 = [[None, None, None], [None, None, None], [None, None, None]]
board3 = [['X', None, None], ['O', 'O', 'X'], ['O', 'X', 'X']]
board4 = [['X', None, None], ['O', 'O', 'X'], ['O', 'X', 'X']]
board5 = [['X', None, None], ['O', 'O', 'X'], ['O', 'X', 'X']]
board6 = [[O, X, EMPTY], [O, X, X], [EMPTY, O, EMPTY]]
board7 = [[EMPTY, EMPTY, EMPTY], [EMPTY, X, EMPTY], [EMPTY, EMPTY, EMPTY]]
board8 = [[EMPTY, EMPTY, EMPTY], [O, X, O], [EMPTY, EMPTY, X]]

boardX = [['X', None, X], ['O', 'O', 'X'], ['O', 'X', 'X']]
boardO = [['X', None, O], ['O', 'O', 'X'], ['O', 'X', 'X']]

minimax(board3)