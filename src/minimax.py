'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Authors:
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison
'''

#|7th.|
def minimax(state, depth=2):
    '''
        Minimax algorithm
    '''

    def max_play(state, alpha, beta, d):
        if state.is_terminal() or d >= depth:
            return state.heuristic_value
        node_value = float('-inf')
        for i, move in enumerate(state.available_moves):
            node_value = max(node_value, min_play(state.next_state(move),
                                                  alpha, beta, d+1))
            if node_value >= beta:
                #print('val:{} move:{}'.format(node_value, move)) # To debug
                return node_value
            alpha = max(alpha, node_value)
        # print('didnt pruned')
        return node_value

    def min_play(state, alpha, beta, d):
        if state.is_terminal() or d >= depth:
            return state.heuristic_value
        node_value = float('inf')
        for i, move in enumerate(state.available_moves):
            node_value = min(node_value, max_play(state.next_state(move),
                                                  alpha, beta, d+1))
            if node_value <= alpha:
                #print('val:{} move:{}'.format(node_value, move)) # To debug
                return node_value
            beta = min(beta, node_value)
        # print('didnt pruned')
        return node_value

    alpha = float('-inf')
    beta = float('inf')
    node_value = float('-inf')
    next_move = state.available_moves[0]
    for i, move in enumerate(state.available_moves):
        neighbor_value = min_play(state.next_state(move), alpha, beta, 1)
        # print('child {}/{}: '.format(i, len(state.available_moves)))
        if neighbor_value > node_value:
            node_value = neighbor_value
            next_move = move
        alpha = max(alpha, node_value)
    return next_move
