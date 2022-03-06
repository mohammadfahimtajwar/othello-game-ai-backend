import random
import time

from othello_shared import get_possible_moves


def select_move(board, color):

    moves = get_possible_moves(board, color)
    i, j = random.choice(moves)

    time.sleep(1)
    return i, j
