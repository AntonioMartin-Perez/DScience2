"""
Tic Tac Toe Player
"""

import math

X       =   "X"
O       =   "O"
EMPTY   =   None


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
    Xs = 0
    for row in board:
        Xs += row.count("X")

    if Xs % 2 == 0:
        turn = X
    else:
        turn = O

    return turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    i = -1
    actions = set()

    for row in board:
        i += 1
        j = -1
        for element in row:
            j +=1
            if element is None:
                actions.add( (i,j) )
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # if action not in actions(board):
    #     raise NotImplementedError
    
    turn            =       player(board)
    i,j             =       action
    # newboard        =       board.copy()
    # newboard        =       list(board)
    newboard        =       [i.copy() for i in board]
    newboard[i][j]  =       turn
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # rows and columns
    for n in range(0,3):
        # print( board[n][:] )
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
    if winner(board) is not None or len( actions(board)) == 0:
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


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


tree = {}
def buildtree(board, parent = None):
    """
    Build the tree with the utility scores in the last nodes
    """

    if terminal(board):
        tree[str(board)] = (utility(board), parent)
        return None


    # construir el árbol de descendientes
    if str(board) not in tree.keys():
        tree[str(board)] = None
    for action in actions(board):
        childboard, parent = result(board, action), board
        buildtree(childboard, parent)

    # print(tree)
    return tree

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # turn = player(board) Creo que va implícito en result

    if terminal(board):
        tree[str(board)] = utility(board)
        return None


    # construir el árbol de descendientes
    if str(board) not in tree.keys():
        tree[str(board)] = None
    for action in actions(board):
        childboard = result(board, action)
        minimax(childboard)

    print(tree)
    # Ahora tengo que propagar los valores hacia arriba




board = [['X', None, None], ['O', 'O', 'X'], ['O', 'X', 'X']]

buildtree(board)