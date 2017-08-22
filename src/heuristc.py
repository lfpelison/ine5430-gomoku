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
    matrix = matrix[1:len(matrix)-1,1:len(matrix)-1].copy() # corta a matrix em uma 15x15
    if player==-1:
        matrix[matrix==0]= 'b'
        matrix[matrix==1]= 'n'     
        matrix[matrix==2]= 'n'
        matrix[matrix==-1]= 'x'
    else:
        matrix[matrix==0]= 'b'
        matrix[matrix==1]= 'x'
        matrix[matrix==2]= 'n'     
        matrix[matrix==-1]= 'n'
    return matrix

    
def makeDig(matrix, player):
    '''
        
    '''
    
    dig = [matrix[::-1,:].diagonal(i) for i in range(-matrix.shape[1]+5,matrix.shape[1]-4)]
    dig_sec=[]
    dig_pri = []    
    #str1='' 
    for i in dig:
        for e in i:
            #print('1')
            if player==-1:
                if e==0:
                    str1 = ''.join('b')
                elif (e==1 or e==2):
                    str1 = ''.join('n')
                elif(e==-1):
                    str1 = ''.join('x')
            else:
                if e==0:
                    str1 = ''.join('b')
                elif (e==-1 or e==2):
                    str1 = ''.join('n')
                elif(e==1):
                    str1 = ''.join('x')       
        dig_sec.append(str1)
        
    dig = [ matrix.diagonal(i) for i in range(matrix.shape[1]-5, -matrix.shape[1]+4,-1) ]
    for i in dig:
        #str2=''
        for e in i:
            #print('2')
            if player==-1:
                if e==0:
                    str2 = ''.join('b')
                elif (e==1 or e==2):
                    str2 = ''.join('n')
                elif(e==-1):
                    str2 = ''.join('x')
            else:
                if e==0:
                    str2 = ''.join('b')
                elif (e==-1 or e==2):
                    str2 = ''.join('n')
                elif(e==1):
                    str2 = ''.join('x')       
        dig_pri.append(str2)
    
    return dig_pri, dig_sec
    

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


    
    
