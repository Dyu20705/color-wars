"""Easy AI for Red: choose a random valid move."""

import random

from src.engine.explosion import resolve_explosions
from src.engine.rules import PLAYER_BLUE, PLAYER_RED, get_move_dot_increment, get_valid_moves


EZ_GREEDY_PROB = 0.10


def _simulate_move(board, dots, move):
    row, col = move
    board_copy = [line[:] for line in board]
    dots_copy = [line[:] for line in dots]

    increment = get_move_dot_increment(board_copy, row, col)
    board_copy[row][col] = PLAYER_RED
    dots_copy[row][col] += increment
    resolve_explosions(board_copy, dots_copy, row, col)
    return board_copy


def _material_score(board):
    score = 0
    for row in board:
        for cell in row:
            if cell == PLAYER_RED:
                score += 1
            elif cell == PLAYER_BLUE:
                score -= 1
    return score


def get_ez_move(board, dots):
    """Pick any valid move. This is intentionally weak."""
    moves = get_valid_moves(board, PLAYER_RED)
    if not moves:
        return None

    if random.random() < EZ_GREEDY_PROB:
        scored = [(move, _material_score(_simulate_move(board, dots, move))) for move in moves]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[0][0]

    return random.choice(moves)