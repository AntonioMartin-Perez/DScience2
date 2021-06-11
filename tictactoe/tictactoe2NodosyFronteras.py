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

class Node():
    def __init__(self, state, parent, turn, utility):
        self.state = state
        self.parent = parent
        # self.action = action
        self.turn = turn
        self.utility = utility


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self): # Devuelve el último nodo de la frontera
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Initialize frontier and tarting position
    start       =       Node( state = board, parent = None, turn = player(board), utility = 0)
    frontier    =       StackFrontier()
    frontier.add(start)
    
    # Initialize explored set
    explored = set()

    # Keep looking while frontier not empty
    while not frontier.empty():
        # pick a node from the frontier and mark it as explored
        node = frontier.remove()
        explored.add( str(node.state) )
        for action in actions(node.state):
            newboard = result( node.state, action )
            if terminal(newboard):
                
            elif str(newboard) not in explored:
                child = Node( state = newboard, parent = node, turn = player( newboard ), utility = 0)
                frontier.add(   child   )

    return explored


################################################## Pruebas ###############################################################
ini = initial_state()
board1 = [[None, X, None], [O, None, X], [None, None, None]]
board2 = [[None, None, None], [None, None, None], [None, None, None]]
board3 = [['X', None, None], ['O', 'O', 'X'], ['O', 'X', 'X']]
board4 = [['X', None, None], ['O', 'O', 'X'], ['O', 'X', 'X']]
board5 = [['X', None, None], ['O', 'O', 'X'], ['O', 'X', 'X']]
boardX = [['X', None, X], ['O', 'O', 'X'], ['O', 'X', 'X']]
boardO = [['X', None, O], ['O', 'O', 'X'], ['O', 'X', 'X']]

minimax(board5)