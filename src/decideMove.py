# -*- coding: utf-8 -*-
"""

@author: Andrei
"""

def decideMove(State, levels=2, PC):
       nextMovement = [0,0]
       heuristic,position =  makeSonsPC(State)
       nextMovement[0],nextMovement[1] = position[np.argmax(heuristic)]
       return nextMovement
    
def minimax(State, size):
  levels= list(range(size))
  
  allStates = []
  allMoves = []
  
  best_move = moves[0]
  best_score = float('-inf')
  for level in levels:
      if level%2==0: #maximizar a chance do pc ganhar
          if level== ( len(levels)-1):
              
          else:
          
      else: #minimizar a chance do adversário ganhar
         if level== ( len(levels)-1):
              
         else:
  
  
  
  
  for move in moves:
    
    if score > best_score:
      best_move = move
      best_score = score
  return best_move
  
def makeSonsPC(State):
    
    State= state.copy()
    allStates= []
     
    for row in range(len(State)):
        for col in range(len(State[row])):
            if (State[row][col]==0):
                newState= State.copy()
                newState[row][col]= self.pc
                allStates.append(newState )
                moves.append([row,col])
                
    return allStates, moves

def makeSonsPlayer(State):
    
    State= state.copy()
    allStates= []
    moves=[]
     
    for row in range(len(State)):
        for col in range(len(State[row])):
            if (State[row][col]==0):
                newState= State.copy()
                newState[row][col]= self.player
                allStates.append(newState )
                moves.append([row,col])
                
    return allStates, moves


def getMax(State, player ): #Assim não precisamos armazenar o estado das folhas que serão calculadas as heuristicas, calculamos direto aqui e armazenamos
    
    State= state.copy()
    heristicOfStates= []
    placeOfStates = []
    
    for row in range(len(State)):
        for col in range(len(State[row])):
            if (State[row][col]==0):
                newState= State.copy()
                newState[row][col]= player
                heristicOfStates.append(calculateHeuristic(newState, self.utility, self.heuristic, player) )
                placeOfStates.append( [row,col ])
                
    return np.argmax(heristicOfStates),placeOfStates[np.argmax(heristicOfStates)] 

def getMin(State, player ):
    
    State= state.copy()
    heristicOfStates= []
    placeOfStates = []
    
    for row in range(len(State)):
        for col in range(len(State[row])):
            if (State[row][col]==0):
                newState= State.copy()
                newState[row][col]= player
                heristicOfStates.append(calculateHeuristic(newState, self.utility, self.heuristic, player) )
                placeOfStates.append( [row,col ])
    return np.argmin(heristicOfStates), placeOfStates[np.argmin(heristicOfStates)] 




