# -*- coding: utf-8 -*-
"""

@author: Andrei
"""
from random import randint
from heuristic import *

use_api= True

def decideMove(State, numberOfPC, numberOfPlayer, levels=2):
        nextMovement = [0,0]
        print("i'm deciding  the move")    
        nextMovement = applyMinimax(State, numberOfPC, numberOfPlayer, levels)
        return nextMovement

def reset():
     #if use_api: 
         
     return np.zeros((15,15))

    
def applyMinimax(State, numberOfPC, numberOfPlayer, levels):

  listOfHeuristics2= []
  listOfHeuristics1= []
  
  listOfStates2= []
  listOfStates1= []
  listOfStates0= []
  listOfStates0.append(State)
  bestHeuristic1 = float('-inf')
  bestState1 = State

  listOfStates1.append( makeSons(listOfStates0[0], numberOfPC) )
  idx = 0 
  for state1 in listOfStates1[0]: #loop for the first level 
      print("I'm on the index of state1: " + str(idx) )
      listOfStates2.append( makeSons(state1, numberOfPlayer) )
      bestState2 = listOfStates2[idx][0]
      bestHeuristic2 = float('+inf')
      idx2 = 0 
      for state2 in listOfStates2[idx]:
               
          hr = -calculateHeuristicValue(state2, numberOfPlayer) + calculateHeuristic(state2, numberOfPC)
          idx2+=1
          if hr < bestHeuristic2:
              bestHeuristic2 = hr
              bestState2 = state2
              
          if bestHeuristic2 > bestHeuristic1:
              bestHeuristic1 = bestHeuristic2
              bestState1 = state2
          if idx>0 and bestHeuristic2 < bestHeuristic1: #alpha prune
              print('Pruned on iteration ' + str(idx2))
              break
              
      listOfHeuristics1.append(bestHeuristic2)
      print("The min heuristic for this state is: " + str(bestHeuristic2) )
      print("--")
      idx +=1
      
      
  
  
      
#  for hr in listOfHeuristics1:
#          
  
  return findMovent(State, bestState1, numberOfPC)
    
    

  
#def makeSons(state, numberToPlayWith):
#    
#    State= state.copy()
#    allStates= []
#      
#    ite = []
#    
#    for i in range(0,8):
#        ite.append( list(range(-i, i+1)) )
#        
##    ite = []
##    old =[[0]]
##    for i in range(0,7):
##        actual = list(range(-i, i+1))
##        ite.append( np.setdiff1d( actual, old) )
##        old = actual
#    
##    for iteration in ite:
##        for row in iteration:
##            for col in iteration:
##                if (State[row+7][col+7]==0):
##                    newState= State.copy()
##                    newState[row+7][col+7]= numberToPlayWith
##                    allStates.append(newState )
#       
#    return allStates

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







