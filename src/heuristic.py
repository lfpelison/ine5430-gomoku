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


Utility = {'numberOfQuintet': [ 200000, ['xxxxx']], 
'numberOfQuartet_2Opens': [ 120000, ['exxxxe']],
'numberOfQuartet_1Open': [ 50000, ['nxxxxe', 'exxxxn']], 
'numberOfTriplet_2Opens': [ 30000, ['exxxe']],
'numberOfTriplet_1Open': [ 15000, ['nxxxee', 'eexxxn']],
'numberOfProbQuartet_2Opens': [ 7000, ['exexxe', 'exxexe']],
'numberOfProbQuartet_1Open': [ 3000, ['nxexxe', 'nxxexe','exxexn','exexxn']],
'numberOfDouble_2Opens': [ 500, ['eexxe', 'exxee']],
'numberOfDouble_1Open': [ 400, ['nxxeee', 'eeexxn']],
'numberOfProbTriplet_2Opens': [ 100, ['exexe']],
'numberOfProbTriplet_1Open': [ 40, ['nxexee', 'eexexn']]
}

#Utility = {
#'numberOfDouble_2Opens': [ 500, ['eexxe', 'exxee']],
#'numberOfDouble_1Open': [ 400, ['nxxeee', 'eeexxn']],
#'numberOfProbTriplet_2Opens': [ 100, ['exexe']],
#'numberOfProbTriplet_1Open': [ 40, ['nxexee', 'eexexn']]
#}



Finished = {'numberOfQuintet': [ 200000, ['xxxxx']]  }


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
 

def finished(state, player, heuristicValues= Finished):
    '''          
         The output is a boolean indicanting if the game finished
         
    '''    
    
    newState = state.copy() #make a matrix 17 x 17
    a= np.asarray([[2 for i in range(15)]]).T
    newState = np.concatenate((a,np.concatenate((newState,a), axis=1)), axis=1).copy()
    a= np.asarray([[2 for i in range(17)]])
    newState = np.concatenate((a,np.concatenate((newState,a), axis=0)), axis=0).copy()
    
    notFinished = True
    occurrences=0
    
    for values in heuristicValues.keys():
        
        
        
        sequence = heuristicValues[values][1]
        #print(values)
        
        for seq in sequence:
            occurrences += searchInList(makeDig(newState, player), seq)
            occurrences += searchInList(makeCol(newState, player), seq)
            occurrences += searchInList(makeLin(newState, player), seq)
            
           
        
        if(values=='numberOfQuintet' and occurrences>0):
            notFinished= False
        
    return notFinished




def calculateHeuristic(state, player, heuristicValues= Utility, positionValuesHeuristic = Heuristic):
    '''  state= numpy matrix of 15x15  with 1's, 0's and -1's meaning the actual 
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
    
    sequenceHeuristic = 0
    positionHeuristic =0
    
    newState = state.copy() #make a matrix 17 x 17
    a= np.asarray([[2 for i in range(15)]]).T
    newState = np.concatenate((a,np.concatenate((newState,a), axis=1)), axis=1).copy()
    a= np.asarray([[2 for i in range(17)]])
    newState = np.concatenate((a,np.concatenate((newState,a), axis=0)), axis=0).copy()
    
    notFinished = True
    
    
    for values in heuristicValues.keys():
        
        
        ValueSequence = heuristicValues[values][0]
        occurrences = 0
        sequence = heuristicValues[values][1]
        #print(values)
        
        for seq in sequence:
            occurrences += searchInList(makeDig(newState, player), seq)
            occurrences += searchInList(makeCol(newState, player), seq)
            occurrences += searchInList(makeLin(newState, player), seq)
            #print(seq)
            #print(occurrences)
            
           
        sequenceHeuristic += occurrences*ValueSequence
        
        
    newState = state.copy() 
    if(player==1):    
        np.place(newState, newState==-1, 0)
        positionHeuristic = np.sum(np.multiply(newState,positionValuesHeuristic))
    else:
        np.place(newState, newState==1,0)
        positionHeuristic = -np.sum(np.multiply(newState,positionValuesHeuristic))
        
    #positionHeuristic=0
    #sequenceHeuristic=0    
     
    HeuristicValue= positionHeuristic + sequenceHeuristic
    return HeuristicValue

    
def makeDig(matrix, player):
    '''
         Make a vector with the diagonals of the matrix 
    '''
    
    dig = [matrix[::-1,:].diagonal(i) for i in range(-matrix.shape[1]+5,matrix.shape[1]-4)]
    diagonal=[]
  
    for i in dig:
        str1=''
        for e in i:
            if player==1:
                if e==0:
                    str1 += 'e'
                elif (e==-1 or e==2):
                    str1 += 'n'
                elif(e==1):
                    str1 +='x' 
            else:
                if e==0:
                    str1 += 'e'
                elif (e==1 or e==2):
                    str1 += 'n'
                elif(e==-1):
                    str1 +='x'     
        diagonal.append(str1)
        
    dig = [ matrix.diagonal(i) for i in range(matrix.shape[1]-5, -matrix.shape[1]+4,-1) ]
    for i in dig:
        str1=''
        for e in i:
            if player==1:
                if e==0:
                    str1 += 'e'
                elif (e==-1 or e==2):
                    str1 += 'n'
                elif(e==1):
                    str1 +='x' 
            else:
                if e==0:
                    str1 += 'e'
                elif (e==1 or e==2):
                    str1 += 'n'
                elif(e==-1):
                    str1 +='x'        
        diagonal.append(str1)
    #print(diagonal)
    
    return diagonal
    

def makeLin(matrix, player):
    '''
         Make a vector with the collumns of the matrix 
    '''
    diagonal=[]
    for i in matrix:
        str1=''
        for e in i:
            
            if player==1:
                if e==0:
                    str1 += 'e'
                elif (e==-1 or e==2):
                    str1 += 'n'
                elif(e==1):
                    str1 +='x' 
            else:
                if e==0:
                    str1 += 'e'
                elif (e==1 or e==2):
                    str1 += 'n'
                elif(e==-1):
                    str1 +='x'       
        diagonal.append(str1)
    #print(diagonal)
    return diagonal
    #matrix = matrix[1:len(matrix)-1,1:len(matrix)-1]
    
def makeCol(matrix, player):
    '''
        Make a vector with the lines of the matrix 
    '''
    diagonal=[]
    matrix = matrix.copy().T
    for i in matrix:
        str1=''
        for e in i:
            
            if player==1:
                if e==0:
                    str1 += 'e'
                elif (e==-1 or e==2):
                    str1 += 'n'
                elif(e==1):
                    str1 +='x' 
            else:
                if e==0:
                    str1 += 'e'
                elif (e==1 or e==2):
                    str1 += 'n'
                elif(e==-1):
                    str1 +='x'       
        diagonal.append(str1)
    #print(diagonal)
    return diagonal
    
    
def searchInList(Lists, searchFor):
    '''
    List: a list of lists with string values
    seachFor: string to search for
    '''
    occurrences=0
    for List in Lists:
        occurrences+= countOccurrences(List, searchFor)
          
    return occurrences
        
    
  
    
def countOccurrences(text, searchFor):
    '''
        Count all occurrences of the string "searchFor" in the text "text"
    '''
    return len(re.findall(searchFor, text, overlapped=True))


    
    
