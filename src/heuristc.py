"""
This code calcutale de heuristc function to the game.

Authors:
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison 
"""

import numpy as np
import regex as re

Utility = {'numberOfQuintet': [quintet, 200000,['xxxxx'] ], 
'numberOfQuartet_2Opens': [quartet_2opens, 120000,['exxxxe']],
'numberOfQuintet': [quintet, 200000, ['xxxxx']], 
'numberOfQuartet_2Opens': [quartet_2opens, 120000, ['exxxxe']],
'numberOfQuartet_1Open': [quartet_1open, 50000, ['nxxxxe', 'exxxxn']], 
'numberOfTriplet_2Opens': [triplet_2opens, 30000, ['exxxe']],
'numberOfTriplet_1Open': [triplet_1open, 15000, ['nxxxee', 'eexxxn']],
'numberOfProbQuartet_2Opens': [prob_quartet_2opens, 7000, ['exexxe', 'exxexe']],
'numberOfProbQuartet_1Open': [prob_quartet_1open, 3000, ['nxexxe', 'nxxexe','exxexn','exexxn']],
'numberOfDouble_2Opens': [double_2opens, 1000, ['eexxe', 'exxee']],
'numberOfDouble_1Open': [double_1open, 400, ['nxxeee', 'eeexxn']],
'numberOfProbTriplet_2Opens': [prob_triplet_2opens, 100, ['exexe']],
'numberOfProbTriplet_1Open': [prob_triplet_1open, 40, ['nxexee', 'eexexn']]
}


Heuristic = [
[0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
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
[0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0]
]
 

def calculateHeuristic(state, heuristicValues, positionValuesHeuristic ):
    '''  state= numpy matrix with 1's, 0's and -1's meaning the actual 
         state of the game
         heuristicValues =  dict with keys with the type of heuristc
         we are searching for, the values are a list. The first element of 
         this list mean the name of function for detction of sequence 
         and values meaning the weight of the sequence.
         Ex:  {'numberOfDoubles': [doubles,1] }
         positionValuesHeuristic = numpy matrix with same dimension of state
         matrix, with the values for heuristic of the pieces positions 
         
         The output is a integer with the value of a heuristc of the state.
         
    '''    
    stateString = changeValues(state)       
        
    sequenceHeuristic = 0
    positionHeuristic =0
    
    for fn in heuristicValues.keys():
        
        numberSequences = heuristicValues[fn][0]()
        
        ValueSequence = heuristicValues[fn][1]
        
        sequenceHeuristic += sequenceHeuristic
        
    
        
    positionHeuristic = np.sum(np.multiply(state,positionValuesHeuristic))
    
    
    HeuristicValue= positionHeuristic + sequenceHeuristic
    return HeuristicValue

def changeValues(matrix, player):
    '''
        This function replace values of the matrix from integer to string 
    
    '''
    matrix = matrix[1:len(matrix)-1,1:len(matrix)-1].copy()
    if player==-1:
        matrix[matrix==-1]= 'b'
        matrix[matrix==1]= 'p'     
        matrix[matrix==0]= 'v'
    else: 
    
    return matrix.

def makeDig(matrix):
    '''
        
    '''
    matrix = matrix[1:len(matrix)-1,1:len(matrix)-1]
    diags_sec = [matrix[::-1,:].diagonal(i) for i in range(-matrix.shape[1]+5,matrix.shape[1]-4)]
    diags_princ = [ matrix.diagonal(i) for i in range(matrix.shape[1]-1, -matrix.shape[1],-1) ]
    list1 = [1, 2, 3]
    str1 = ''.join(str(e) for e in list1)
    print([n.tolist() for n in diags_sec])
    #print([n.tolist() for n in diags_princ])
    

def makeCol(matrix):
    '''
    '''
    matrix = matrix[1:len(matrix)-1,1:len(matrix)-1]
    
def makeLin(matrix):
    '''
    '''
    matrix = matrix[1:len(matrix)-1,1:len(matrix)-1]
    
def quintet(stateString):
    

    
    
def countOccurrences(text, search_for):
    return len(re.findall(search_for, text, overlapped=True))


    
    
