'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Authors:
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison
File description:
    This module implements a heuristic function for the game.
'''
import numpy as np
import regex as re


UTILITY = {'Quintet': [20000000, ['xxxxx']],
           'Quartet_2Opens': [400000, ['exxxxe']],
           'Quartet_1Open': [50000, ['nxxxxe', 'exxxxn']],
           'Triplet_2Opens': [30000, ['exxxe']],
           'Triplet_1Open': [15000, ['nxxxee', 'eexxxn']],
           'ProbQuartet_2Opens': [7000, ['exexxe', 'exxexe']],
           'ProbQuartet_1Open': [3000, ['nxexxe',
                                                'nxxexe', 'exxexn', 'exexxn']],
           'Double_2Opens': [500, ['eexxe', 'exxee']],
           'Double_1Open': [400, ['nxxeee', 'eeexxn']],
           'nProbTriplet_2Opens': [100, ['exexe']],
           'ProbTriplet_1Open': [40, ['nxexee', 'eexexn']]}

FINISHED = {'Quintet': [200000, ['xxxxx']]}

HEURISTIC = [[0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0]]


#|21th.|
def hasWinnerSeq(board, lastPlayer, winnerSeq='xxxxx'):
    '''
         The output is a boolean indicating if the board has a winner sequence.

    '''
    newBoard = board.copy()
    a = np.asarray([[2 for i in range(15)]]).T
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=1)),
                              axis=1).copy()
    a = np.asarray([[2 for i in range(17)]])
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=0)),
                              axis=0).copy()
    count = 0
    count += searchInList(makeDig(newBoard, lastPlayer), winnerSeq)
    count += searchInList(makeCol(newBoard, lastPlayer), winnerSeq)
    count += searchInList(makeLin(newBoard, lastPlayer), winnerSeq)
    if count > 0:
        return True
    else:
        return False


#|10th.|
def calculateHeuristic(board,
                       player,
                       heuristicValues=UTILITY,
                       positionValuesHeuristic=HEURISTIC):
    '''
         This function calculates the heuristic of sosme move
         board= numpy matrix of 15x15  with 1's, 0's and -1's meaning the actual
         board of the game
         heuristicValues =  dict with keys with the type of heuristc
         we are searching for.
         positionValuesHeuristic = numpy matrix with same dimension of board
         matrix, with the values for heuristic of the pieces positions
         number_to_play_with= -1 or 1, depeding if we are calculating the pc heuristic or the player heuristic
         pc_number = 1 ot -1, value that the pc are playing

         The output is a integer with the value of a heuristc of the board.

    '''
    sequenceHeuristic = 0
    positionHeuristic = 0
    newBoard = board.copy()
    a = np.asarray([[2 for i in range(15)]]).T
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=1)),
                              axis=1).copy()
    a = np.asarray([[2 for i in range(17)]])
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=0)),
                              axis=0).copy()
    for values in heuristicValues.keys():
        ValueSequence = heuristicValues[values][0]
        count = 0
        sequence = heuristicValues[values][1]
        for seq in sequence:
            count += searchInList(makeDig(newBoard, player), seq)
            count += searchInList(makeCol(newBoard, player), seq)
            count += searchInList(makeLin(newBoard, player), seq)
        sequenceHeuristic += count*ValueSequence
    newBoard = board.copy()
    if(player == 1):
        np.place(newBoard, newBoard == -1, 0)
        positionHeuristic = np.sum(np.multiply(newBoard,
                                               positionValuesHeuristic))
    else:
        np.place(newBoard, newBoard == 1, 0)
        positionHeuristic = -np.sum(np.multiply(newBoard,
                                                positionValuesHeuristic))
    HeuristicValue = positionHeuristic + sequenceHeuristic

    total = HeuristicValue





    player = -1*player
    sequenceHeuristic = 0
    positionHeuristic = 0
    newBoard = board.copy()
    a = np.asarray([[2 for i in range(15)]]).T
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=1)),
                              axis=1).copy()
    a = np.asarray([[2 for i in range(17)]])
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=0)),
                              axis=0).copy()
    for values in heuristicValues.keys():
        ValueSequence = heuristicValues[values][0]
        count = 0
        sequence = heuristicValues[values][1]
        for seq in sequence:
            count += searchInList(makeDig(newBoard, player), seq)
            count += searchInList(makeCol(newBoard, player), seq)
            count += searchInList(makeLin(newBoard, player), seq)
        sequenceHeuristic += count*ValueSequence
    newBoard = board.copy()
    if(player == 1):
        np.place(newBoard, newBoard == -1, 0)
        positionHeuristic = np.sum(np.multiply(newBoard,
                                               positionValuesHeuristic))
    else:
        np.place(newBoard, newBoard == 1, 0)
        positionHeuristic = -np.sum(np.multiply(newBoard,
                                                positionValuesHeuristic))
    HeuristicValue = positionHeuristic + sequenceHeuristic
    return total - 1.05*HeuristicValue #PC heuristics versus - Human heuristics with a gain


#|11th.|
def makeDig(matrix, player):
    '''
         Make a vector with the diagonals of the matrix
    '''
    dig = [matrix[::-1, :].diagonal(i) for i in range(-matrix.shape[1] + 5,
                                                      matrix.shape[1] - 4)]
    diagonal = []
    for i in dig:
        str1 = ''
        for e in i:
            if player == 1:
                if e == 0:
                    str1 += 'e'
                elif (e == -1 or e == 2):
                    str1 += 'n'
                elif(e == 1):
                    str1 += 'x'
            else:
                if e == 0:
                    str1 += 'e'
                elif (e == 1 or e == 2):
                    str1 += 'n'
                elif(e == -1):
                    str1 += 'x'
        diagonal.append(str1)
    dig = [matrix.diagonal(i) for i in range(matrix.shape[1]-5,
                                             -matrix.shape[1] + 4, -1)]
    for i in dig:
        str1 = ''
        for e in i:
            if player == 1:
                if e == 0:
                    str1 += 'e'
                elif (e == -1 or e == 2):
                    str1 += 'n'
                elif(e == 1):
                    str1 += 'x'
            else:
                if e == 0:
                    str1 += 'e'
                elif (e == 1 or e == 2):
                    str1 += 'n'
                elif(e == -1):
                    str1 += 'x'
        diagonal.append(str1)
    return diagonal


#|15th.|
def makeLin(matrix, player):
    '''
         Make a vector with the collumns of the matrix
    '''
    diagonal = []
    for i in matrix:
        str1 = ''
        for e in i:
            if player == 1:
                if e == 0:
                    str1 += 'e'
                elif (e == -1 or e == 2):
                    str1 += 'n'
                elif(e == 1):
                    str1 += 'x'
            else:
                if e == 0:
                    str1 += 'e'
                elif (e == 1 or e == 2):
                    str1 += 'n'
                elif(e == -1):
                    str1 += 'x'
        diagonal.append(str1)
    return diagonal


#|14th.|
def makeCol(matrix, player):
    '''
        Make a vector with the lines of the matrix
    '''
    diagonal = []
    matrix = matrix.copy().T
    for i in matrix:
        str1 = ''
        for e in i:
            if player == 1:
                if e == 0:
                    str1 += 'e'
                elif (e == -1 or e == 2):
                    str1 += 'n'
                elif(e == 1):
                    str1 += 'x'
            else:
                if e == 0:
                    str1 += 'e'
                elif (e == 1 or e == 2):
                    str1 += 'n'
                elif(e == -1):
                    str1 += 'x'
        diagonal.append(str1)
    return diagonal


#|12th.|
def searchInList(Lists, searchFor):
    '''
    List: a list of lists with string values
    seachFor: string to search for
    '''
    count = 0
    for List in Lists:
        count += countOccurrences(List, searchFor)
    return count


#|13th.|
def countOccurrences(text, searchFor):
    '''
        Count all occurrences of the string "searchFor" in the text "text"
    '''
    return len(re.findall(searchFor, text, overlapped=True))
