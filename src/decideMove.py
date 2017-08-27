# -*- coding: utf-8 -*-
"""

@author: Andrei
"""
from random import randint
from heuristic import *

def decideMove(State, numberOfPC, numberOfPlayer, levels=2):
       nextMovement = [0,0]
       print("i'm deciding  the move")
       nextMovement = applyMinimax(State, numberOfPC, numberOfPlayer, levels)
       return nextMovement

    
def applyMinimax(State, numberOfPC, numberOfPlayer, levels):

  listOfHeuristics2= []
  listOfHeuristics1= []
  
  listOfStates2= []
  listOfStates1= []
  listOfStates0= []
  listOfStates0.append(State)

  listOfStates1.append( makeSons(listOfStates0[0], numberOfPC) )
  idx = 0 
  for state1 in listOfStates1[0]: #loop for the first level 
      print("I'm on the index of state1:" + str(idx) )
      listOfStates2.append( makeSons(state1, numberOfPlayer) )
      bestState = listOfStates2[idx][0]
      bestHeuristic = float('+inf')
      idx2 = 0 
      for state2 in listOfStates2[idx]:
          hr = -calculateHeuristicValue(state2, numberOfPlayer) + calculateHeuristic(state2, numberOfPC)
          idx2+=1
          if hr < bestHeuristic:
              bestHeuristic = hr
              bestState = state2
              
      listOfHeuristics1.append(bestHeuristic)
      print("The min heuristic for this state is:" + str(bestHeuristic) )
      print("--")
      
      idx +=1
      
  bestState = listOfStates1[0][0]
  
  bestHeuristic = float('-inf')    
  for hr in listOfHeuristics1:
          if hr > bestHeuristic:
              bestHeuristic = hr
              bestState = listOfStates1[0][listOfHeuristics1.index(hr)]
  
  return findMovent(State, bestState, numberOfPC)
    
    

  
def makeSons(state, numberToPlayWith):
    
    State= state.copy()
    allStates= []
     
    for row in range(len(State)):
        for col in range(len(State[row])):
            if (State[row][col]==0):
                newState= State.copy()
                newState[row][col]= numberToPlayWith
                allStates.append(newState )
                
                
    return allStates


def calculateHeuristicValue(state, player):
    return calculateHeuristic(state, player)  


def hasFinished(state, player):
    return finished(state, player)


def findMovent(actualState,nextMove, numberToPlayWith):
        row, col = np.where( (actualState+nextMove)==numberToPlayWith) 
        
        return [row[0], col[0]]







