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
    """
    Returns player who has the next turn on a board.
    """

    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count += 1
            elif board[i][j] == O:
                count -= 1
    if count == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    acts = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                acts.add((i, j))
    return acts

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    b = copy.deepcopy(board)
    b[action[0]][action[1]] = player(board)

    return b


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        """
        The win checking works by using 2 counters, one for rows and one for coumns
        If at the end of the row or column the counter has counted 3 Xs or 3 Os then
        if it counted to +3 then X won and if it counted to -3 O wons
        I and J are not rows and columns because counter x and counter y use them differently
        """
        counterx = 0
        countery = 0
        for j in range(3):
            if board[i][j] == X:
                counterx += 1
            elif board[i][j] == O:
                counterx -= 1
            if board[j][i] == X:
                countery += 1
            elif board[j][i] == O:
                countery -= 1
        if counterx == 3 or countery == 3:
            return X
        elif counterx == -3 or countery == -3:
            return O
        
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
        
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if player(board) == X:
        return findMax(board)[1]
    else:
        return findMin(board)[1]



def findMax(board):
    if terminal(board):
        return None    
        
    max = -2
    options = actions(board)
    best = None
    for move in options:

        r = result(board, move)
        u = None
        if terminal(r) == True:
            u = utility(r)
            if u > max:
                max = u
                best = move
        else:
            v = findMin(r)
            if v[0] > max:
                max = v[0]
                best = move
        if max == 1:
            return(max, best)
    if best == None:
        best = actions(board).pop
    return (max, best)

def findMin(board):
    if terminal(board):
        return None
        
    min = 2
    options = actions(board)
    best = None
    for move in options:
        r = result(board, move)
        u = None
        if terminal(r) == True:
            u = utility(r)
            if u < min:
                min = u
                best = move
        else:
            v = findMax(r)
            if v[0] < min:
                min = v[0]
                best = move
        if min == -1:
            return(min, best)
    if best == None:
        o = actions(board)
        best = o.pop() 
    return (min, best)