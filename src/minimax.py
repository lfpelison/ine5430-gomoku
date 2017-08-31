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


def decideMove(State, numberOfPC, numberOfPlayer, levels=2):
        nextMovement = [0, 0]
        print("thinking...")
        nextMovement = applyMinimax(State, numberOfPC, numberOfPlayer, levels)
        return nextMovement


def reset():
    return np.zeros((15, 15))


def applyMinimax(State, numberOfPC, numberOfPlayer, levels):
    listOfHeuristics1 = []
    listOfStates2 = []
    listOfStates1 = []
    listOfStates0 = []
    listOfStates0.append(State)
    bestHeuristic1 = float('-inf')
    bestState1 = State
    listOfStates1.append(makeChildren(listOfStates0[0], numberOfPC))
    idx = 0
    for state1 in listOfStates1[0]:  # loop for the first level
        listOfStates2.append(makeChildren(state1, numberOfPlayer))
        bestState2 = listOfStates2[idx][0]
        bestHeuristic2 = float('+inf')
        idx2 = 0
        for state2 in listOfStates2[idx]:
            hr = -calculateHeuristicValue(state2,
                                          numberOfPlayer) + calculateHeuristic(
                                                              state2,
                                                              numberOfPC)
            idx2 += 1
            if hr < bestHeuristic2:
                bestHeuristic2 = hr
                bestState2 = state2
            if bestHeuristic2 > bestHeuristic1:
                bestHeuristic1 = bestHeuristic2
                bestState1 = state2
            if idx > 0 and bestHeuristic2 < bestHeuristic1:  # alpha prune
                # print('Pruned on iteration ' + str(idx2))
                break
        listOfHeuristics1.append(bestHeuristic2)
        # print("idx: " + str(idx) +" - pr:" + str(idx2)+" - bt hr: "  + str(bestHeuristic1) )
        idx += 1
    return findMovent(State, bestState1, numberOfPC)


def makeChildren(state, numberToPlayWith):
    currState = state.copy()
    proxState = currState.copy()
    proxMatrix = np.ones((5, 5))*3
    for row in range(currState.shape[0]-4):
        for col in range(currState.shape[1]-4):
            if np.any(currState[row:row+5, col:col+5]):
                proxState[row:row+5, col:col+5] += proxMatrix
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


def calculateHeuristicValue(state, player):
    return calculateHeuristic(state, player)


def findMovent(actualState, nextMove, numberToPlayWith):
        row, col = np.where((actualState + nextMove) == numberToPlayWith)
        return [row[0], col[0]]
