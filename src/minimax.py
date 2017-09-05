'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Authors:
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison
'''
import numpy as np


def minimax(state, pcNumber, playerNumber, depth=3):
    '''
    Apply the minimax algorithm using the heuristic function.
    
    Return a array with the row and the column with the best move for the PC
    '''
    player = state.player

    def max_play(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_play(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    action, state = argmax(game.successors(state),
                           lambda a, s: min_value(s, -infinity, infinity, 0))
    return action
    
    
    
    '''
    listOfHeuristics1 = []
    listOfStates2 = []
    listOfStates1 = []
    listOfStates0 = []
    listOfStates0.append(State)
    bestHeuristic1 = float('-inf')
    bestState1 = State
    listOfStates1.append(makeChildren(listOfStates0[0], pcNumber))
    idx = 0
    son1 = len(listOfStates1[0])
    for state1 in listOfStates1[0]:  # loop for the first level
        listOfStates2.append(makeChildren(state1, playerNumber))
        bestState2 = listOfStates2[idx][0]
        bestHeuristic2 = float('+inf')
        idx2 = 0
        son2 = len(listOfStates2[idx])
        for state2 in listOfStates2[idx]:
            hr = -calculateHeuristic(state2, playerNumber) + calculateHeuristic( state2, pcNumber)
            idx2 += 1
            if hr < bestHeuristic2:
                bestHeuristic2 = hr
                bestState2 = state2
            if bestHeuristic2 > bestHeuristic1:
                bestHeuristic1 = bestHeuristic2
                bestState1 = state2
            if idx > 0 and bestHeuristic2 < bestHeuristic1:  # alpha prune
                break
        listOfHeuristics1.append(bestHeuristic2)
        print("Iteration: " + str(idx+1) +"/"+ str(son1) +  " - Pruned at:" + str(idx2)+"/"+ str(son2) )
        idx += 1
    return findMovent(State, bestState1, pcNumber)
'''

def makeChildren(state, numberToPlayWith):
    self.board = state.copy()
    proximityBoard = self.board.copy()
    temp = np.count_nonzero(proximityBoard)
    if ( temp>1 ):
        proximityMatrix = np.ones((5, 5))*3
        for row in range(self.board.shape[0]-4):
            for col in range(self.board.shape[1]-4):
                if np.any(self.board[row:row+5, col:col+5]):
                    proximityBoard[row:row+5, col:col+5] += proximityMatrix
    elif temp==1 and self.board[7][7]==0 : 
        proximityBoard[7,7]= 3
    elif temp==1 and self.board[7][7]!=0 : 
        proximityBoard[6,6]= 3
    elif temp==0 : 
        proximityBoard[7,7]= 3
        
    allStates = []
    diffToCenter = abs(np.arange(len(self.board)) - int(len(self.board)/2))
    centerToBorder = np.argsort(diffToCenter)
    for row in centerToBorder:
        for col in centerToBorder:
            if (proximityBoard[row][col] % 3 == 0 and proximityBoard[row][col] > 0):
                newState = self.board.copy()
                newState[row][col] = numberToPlayWith
                allStates.append(newState)
    return allStates


def findMovent(self.board, nextMove, numberToPlayWith):
        row, col = np.where((self.board + nextMove) == numberToPlayWith)
        return [row[0], col[0]]
