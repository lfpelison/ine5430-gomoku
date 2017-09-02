'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Authors:
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison
'''
from heuristic import calculateHeuristic
import numpy as np


def decideMove(State, numberOfPC, numberOfPlayer):
        nextMovement = [0, 0]
        print("I'm deciding  the move. It may take a while! ")    
        nextMovement = minimax(State, numberOfPC, numberOfPlayer)
        return nextMovement


def reset():
    return np.zeros((15, 15))


def minimax(State, numberOfPC, numberOfPlayer):
    '''
    Apply the minimax algorith using the heuristic function.
    
    Return a array with the row and the column with the best move for the PC
    '''
    listOfHeuristics1 = []
    listOfStates2 = []
    listOfStates1 = []
    listOfStates0 = []
    listOfStates0.append(State)
    bestHeuristic1 = float('-inf')
    bestState1 = State
    listOfStates1.append(makeChildren(listOfStates0[0], numberOfPC))
    idx = 0
    son1 = len(listOfStates1[0])
    for state1 in listOfStates1[0]:  # loop for the first level
        listOfStates2.append(makeChildren(state1, numberOfPlayer))
        bestState2 = listOfStates2[idx][0]
        bestHeuristic2 = float('+inf')
        idx2 = 0
        son2 = len(listOfStates2[idx])
        for state2 in listOfStates2[idx]:
            hr = -calculateHeuristic(state2, numberOfPlayer) + calculateHeuristic( state2, numberOfPC)
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
    return findMovent(State, bestState1, numberOfPC)


def makeChildren(state, numberToPlayWith):
    currState = state.copy()
    proxState = currState.copy()
    temp = np.count_nonzero(proxState)
    if ( temp>1 ):
        proxMatrix = np.ones((5, 5))*3
        for row in range(currState.shape[0]-4):
            for col in range(currState.shape[1]-4):
                if np.any(currState[row:row+5, col:col+5]):
                    proxState[row:row+5, col:col+5] += proxMatrix
    elif temp==1 and currState[7][7]==0 : 
        proxState[7,7]= 3
    elif temp==1 and currState[7][7]!=0 : 
        proxState[6,6]= 3
    elif temp==0 : 
        proxState[7,7]= 3
        
    allStates = []
    diffToCenter = abs(np.arange(len(currState)) - int(len(currState)/2))
    centerToBorder = np.argsort(diffToCenter)
    for row in centerToBorder:
        for col in centerToBorder:
            if (proxState[row][col] % 3 == 0 and proxState[row][col] > 0):
                newState = currState.copy()
                newState[row][col] = numberToPlayWith
                allStates.append(newState)
    return allStates


def findMovent(currState, nextMove, numberToPlayWith):
        row, col = np.where((currState + nextMove) == numberToPlayWith)
        return [row[0], col[0]]
