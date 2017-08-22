"""
This code calcutale de heuristc function to the game.

Authors:
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison 
"""

import numpy as np
import regex as re

Utility = {'numberOfQuintet': [ 200000, ['xxxxx']], 
'numberOfQuartet_2Opens': [ 120000, ['exxxxe']],
'numberOfQuartet_1Open': [ 50000, ['nxxxxe', 'exxxxn']], 
'numberOfTriplet_2Opens': [ 30000, ['exxxe']],
'numberOfTriplet_1Open': [ 15000, ['nxxxee', 'eexxxn']],
'numberOfProbQuartet_2Opens': [ 7000, ['exexxe', 'exxexe']],
'numberOfProbQuartet_1Open': [ 3000, ['nxexxe', 'nxxexe','exxexn','exexxn']],
'numberOfDouble_2Opens': [ 1000, ['eexxe', 'exxee']],
'numberOfDouble_1Open': [ 400, ['nxxeee', 'eeexxn']],
'numberOfProbTriplet_2Opens': [ 100, ['exexe']],
'numberOfProbTriplet_1Open': [ 40, ['nxexee', 'eexexn']]
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
    
    for values in heuristicValues.keys():
        
        sequence = heuristicValues[values][1]
        
        ValueSequence = heuristicValues[values][0]
        
        sequenceHeuristic += sequenceHeuristic
        
    
        
    positionHeuristic = np.sum(np.multiply(state,positionValuesHeuristic))
    
    
    HeuristicValue= positionHeuristic + sequenceHeuristic
    return HeuristicValue

    
def makeDig(matrix, player):
    '''
        
    '''
    
    dig = [matrix[::-1,:].diagonal(i) for i in range(-matrix.shape[1]+5,matrix.shape[1]-4)]
    diagonal=[]
  
    for i in dig:
        str1=''
        for e in i:
            
            if player==1:
                if e==0:
                    str1 += 'b'
                elif (e==1 or e==2):
                    str1 += 'n'
                elif(e==-1):
                    str1 +='x' 
            else:
                if e==0:
                    str1 = ''.join('b')
                elif (e==-1 or e==2):
                    str1 = ''.join('n')
                elif(e==1):
                    str1 = ''.join('x')       
        diagonal.append(str1)
        
    dig = [ matrix.diagonal(i) for i in range(matrix.shape[1]-5, -matrix.shape[1]+4,-1) ]
    for i in dig:
        str1=''
        for e in i:
            if player==1:
                if e==0:
                    str1 += 'b'
                elif (e==1 or e==2):
                    str1 += 'n'
                elif(e==-1):
                    str1 +='x' 
            else:
                if e==0:
                    str1 = ''.join('b')
                elif (e==-1 or e==2):
                    str1 = ''.join('n')
                elif(e==1):
                    str1 = ''.join('x')       
        diagonal.append(str1)
    
    return diagonal
    

def makeCol(matrix, player):
    '''
    '''
    diagonal=[]
    for i in matrix:
        str1=''
        for e in i:
            
            if player==1:
                if e==0:
                    str1 += 'b'
                elif (e==1 or e==2):
                    str1 += 'n'
                elif(e==-1):
                    str1 +='x' 
            else:
                if e==0:
                    str1 = ''.join('b')
                elif (e==-1 or e==2):
                    str1 = ''.join('n')
                elif(e==1):
                    str1 = ''.join('x')       
        diagonal.append(str1)
    return diagonal
    #matrix = matrix[1:len(matrix)-1,1:len(matrix)-1]
    
def makeLin(matrix, player):
    '''
    '''
    diagonal=[]
    matrix = matrix.copy().T
    for i in matrix:
        str1=''
        for e in i:
            
            if player==1:
                if e==0:
                    str1 += 'b'
                elif (e==1 or e==2):
                    str1 += 'n'
                elif(e==-1):
                    str1 +='x' 
            else:
                if e==0:
                    str1 = ''.join('b')
                elif (e==-1 or e==2):
                    str1 = ''.join('n')
                elif(e==1):
                    str1 = ''.join('x')       
        diagonal.append(str1)
    return diagonal
    
  
    
def countOccurrences(text, search_for):
    return len(re.findall(search_for, text, overlapped=True))


    
    
