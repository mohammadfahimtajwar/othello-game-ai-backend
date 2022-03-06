import time
import timeout_decorator

from constants import TIME_OUT
from othello_shared import get_possible_moves, play_move, compute_utility


def minimax_max_node(board):

    moves = get_possible_moves(board, 1)

    if len(moves) == 0:
        return compute_utility(board)

    v = float('-inf')

    for i in range(0, len(moves)):
        x, y = moves[i]
        v = max(v, minimax_min_node(play_move(board, 1, x, y)))

    return v


def minimax_min_node(board):

    moves = get_possible_moves(board, 2)

    if len(moves) == 0:
        return compute_utility(board)

    v = float('inf')

    for i in range(0, len(moves)):
        x, y = moves[i]
        v = min(v, minimax_max_node(play_move(board, 2, x, y)))

    return v


@timeout_decorator.timeout(TIME_OUT, use_signals=False)
def select_move_minimax(board, color):

    moves = get_possible_moves(board, color)
    utilities = []

    if color == 1:

        for i in range(0, len(moves)):
            x, y = moves[i]
            utilities.append(minimax_min_node(play_move(board, 1, x, y)))
        time.sleep(1)
        return moves[utilities.index(max(utilities))]

    else:

        for i in range(0, len(moves)):
            x, y = moves[i]
            utilities.append(minimax_max_node(play_move(board, 2, x, y)))

        time.sleep(1)

        return moves[utilities.index(min(utilities))]
