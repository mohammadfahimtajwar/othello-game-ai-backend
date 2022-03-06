import heapq
import time
import timeout_decorator
from constants import TIME_OUT
from othello_shared import get_possible_moves, play_move, compute_utility


def alphabeta_max_node(board, alpha, beta, level=1, limit=float("inf")):

    moves = get_possible_moves(board, 1)

    if len(moves) == 0:
        return compute_utility(board)

    utilities = []

    for i in range(0, len(moves)):
        x, y = moves[i]
        utilities.append(compute_utility(play_move(board, 1, x, y)))

    utilities = [-i for i in utilities]
    ordered_set = [(utilities[i], moves[i]) for i in range(len(moves))]
    heapq.heapify(ordered_set)
    ordered_moves = [ordered_set[i][1] for i in range(len(ordered_set))]

    v = float('-inf')

    for i in range(len(ordered_moves)):

        x, y = ordered_moves[i]

        if level < limit:

            v = max(v, alphabeta_min_node(play_move(board, 1, x, y), alpha, beta, level + 1, limit))

        else:

            v = max(v, compute_utility(board))

        if v >= beta:
            return v

        alpha = max(alpha, v)

    return v


def alphabeta_min_node(board, alpha, beta, level=1, limit=float("inf")):
    moves = get_possible_moves(board, 2)

    if len(moves) == 0:
        return compute_utility(board)

    utilities = []

    for i in range(0, len(moves)):
        x, y = moves[i]
        utilities.append(compute_utility(play_move(board, 2, x, y)))

    ordered_set = [(utilities[i], moves[i]) for i in range(len(moves))]
    heapq.heapify(ordered_set)
    ordered_moves = [ordered_set[i][1] for i in range(len(ordered_set))]

    v = float('inf')

    for i in range(0, len(ordered_moves)):

        x, y = ordered_moves[i]

        if level < limit:

            v = min(v, alphabeta_max_node(play_move(board, 2, x, y), alpha, beta, level + 1, limit))

        else:

            v = min(v, compute_utility(board))

        if v <= alpha:
            return v

        beta = min(beta, v)

    return v


@timeout_decorator.timeout(TIME_OUT, use_signals=False)
def select_move_alphabeta(board, color, limit=float("inf")):

    moves = get_possible_moves(board, color)
    utilities = []

    if color == 1:

        for i in range(0, len(moves)):
            x, y = moves[i]
            utilities.append(alphabeta_min_node(play_move(board, 1, x, y), float('-inf'), float('inf'), 2, limit))
        time.sleep(1)
        return moves[utilities.index(max(utilities))]

    else:

        for i in range(0, len(moves)):
            x, y = moves[i]
            utilities.append(alphabeta_max_node(play_move(board, 2, x, y), float('-inf'), float('inf'), 2, limit))

        time.sleep(1)

        return moves[utilities.index(min(utilities))]
