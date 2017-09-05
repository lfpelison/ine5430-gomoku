'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Authors:
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison
'''
def minimax(state, depth=0):
    '''
        Minimax algorithm
    '''

    def max_play(state, alpha, beta, d):
        if state.is_terminal() or d > depth:
            return state.heuristic_value
        node_value = float('-inf')
        for move in state.available_moves:
            node_value = max(node_value, min_play(state.next_state(move), 
                                                  alpha, beta, d+1))
            if node_value >= beta:
                print('pruned on max')
                return node_value
            alpha = max(alpha, node_value)
        print('return from {}'.format(d))
        return node_value

    def min_play(state, alpha, beta, d):
        if state.is_terminal() or d > depth:
            return state.heuristic_value
        node_value = float('inf')
        for move in state.available_moves:
            node_value = min(node_value, max_play(state.next_state(move), 
                                                  alpha, beta, d+1))
            if node_value <= alpha:
                print('pruned on min')
                return node_value
            beta = min(beta, node_value)
        print('return from {}'.format(d))
        return node_value
    
    firstLayer = map(lambda move: (move, min_play(state.next_state(move), 
                                                  float('-inf'), 
                                                  float('inf'), 0)), 
                     state.available_moves)
    move = max(firstLayer, key=lambda x: x[1])[0]
    return move
      