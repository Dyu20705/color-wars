"""Benchmark AI matchup win rates with mirrored color handling.

Usage:
    python scripts/benchmark_ai.py --games 200
"""

from __future__ import annotations

import argparse
import random
from collections import Counter
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ai.ez_AI import get_ez_move
from src.ai.hard_AI import get_hard_move
from src.ai.med_AI import get_med_move
from src.controller import apply_move, get_scores
from src.engine.rules import EMPTY, PLAYER_BLUE, PLAYER_RED
from src.game.state import GameState


AI_BY_NAME = {
    "easy": get_ez_move,
    "medium": get_med_move,
    "hard": get_hard_move,
}


def swap_board(board: list[list[int]]) -> list[list[int]]:
    return [
        [EMPTY if cell == EMPTY else (PLAYER_BLUE if cell == PLAYER_RED else PLAYER_RED) for cell in row]
        for row in board
    ]


def choose_move(ai_name: str, board: list[list[int]], dots: list[list[int]]):
    return AI_BY_NAME[ai_name](board, dots)


def play_game(blue_ai: str, red_ai: str, seed: int, start_player: int, max_turns: int = 300):
    random.seed(seed)

    state = GameState()
    state.current_player = start_player
    turns = 0

    while state.winner is None and turns < max_turns:
        if state.current_player == PLAYER_RED:
            move = choose_move(red_ai, state.board, state.dots)
            if move is None:
                blue_score, red_score = get_scores(state)
                if red_score == 0 and blue_score > 0:
                    state.winner = PLAYER_BLUE
                elif blue_score == 0 and red_score > 0:
                    state.winner = PLAYER_RED
                else:
                    state.current_player = PLAYER_BLUE
            else:
                apply_move(state, move[0], move[1], player=PLAYER_RED)
        else:
            move = choose_move(blue_ai, swap_board(state.board), state.dots)
            if move is None:
                blue_score, red_score = get_scores(state)
                if red_score == 0 and blue_score > 0:
                    state.winner = PLAYER_BLUE
                elif blue_score == 0 and red_score > 0:
                    state.winner = PLAYER_RED
                else:
                    state.current_player = PLAYER_RED
            else:
                apply_move(state, move[0], move[1], player=PLAYER_BLUE)

        turns += 1

    blue_score, red_score = get_scores(state)
    return state.winner, blue_score, red_score, turns


def bench_matchup(blue_ai: str, red_ai: str, games: int, seed: int):
    results = Counter()
    score_diffs = []
    turn_counts = []

    for index in range(games):
        start_player = PLAYER_BLUE if index % 2 == 0 else PLAYER_RED
        winner, blue_score, red_score, turns = play_game(
            blue_ai=blue_ai,
            red_ai=red_ai,
            seed=seed + index,
            start_player=start_player,
        )
        results[winner] += 1
        score_diffs.append(blue_score - red_score)
        turn_counts.append(turns)

    total = max(1, games)
    return {
        "blue_ai": blue_ai,
        "red_ai": red_ai,
        "blue_winrate": results[PLAYER_BLUE] / total,
        "red_winrate": results[PLAYER_RED] / total,
        "draw_rate": results[None] / total,
        "avg_score_diff": sum(score_diffs) / total,
        "avg_turns": sum(turn_counts) / total,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    matchups = [
        ("easy", "medium"),
        ("medium", "medium"),
        ("medium", "hard"),
        ("hard", "medium"),
        ("easy", "hard"),
        ("hard", "easy"),
    ]

    for blue_ai, red_ai in matchups:
        stats = bench_matchup(blue_ai, red_ai, games=args.games, seed=args.seed)
        print(
            f"{blue_ai:>6} vs {red_ai:<6} | "
            f"blue {stats['blue_winrate']:.1%} | red {stats['red_winrate']:.1%} | "
            f"draw {stats['draw_rate']:.1%} | avg turns {stats['avg_turns']:.1f} | "
            f"avg score diff {stats['avg_score_diff']:.2f}"
        )


if __name__ == "__main__":
    main()