"""High-level scene composition for the game view."""

from src.engine.rules import PLAYER_BLUE

from .board import drawBoard
from .constants import BG_BLUE_TURN, BG_NEUTRAL, BG_RED_TURN
from .hud import drawHud
from .layout import compute_layout


def drawScene(screen, board, dots, current_player, blue_score, red_score, winner, game_mode=None, difficulty=None):
    """Render one complete frame."""
    layout = compute_layout(screen, len(board))
    if winner is None:
        bg_color = BG_BLUE_TURN if current_player == PLAYER_BLUE else BG_RED_TURN
    else:
        bg_color = BG_NEUTRAL
    screen.fill(bg_color)
    drawBoard(screen, board, dots, layout)
    drawHud(screen, current_player, blue_score, red_score, winner, game_mode, difficulty, layout)