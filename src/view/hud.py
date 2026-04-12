"""Heads-up display rendering."""

import pygame

from src.engine.rules import PLAYER_BLUE

from .constants import BLUE_COLOR, HUD_TEXT_COLOR, RED_COLOR


def _render_fitted_line(text, color, preferred_size, min_size, max_width):
    """Render a line that fits the available width."""
    font_size = preferred_size
    while font_size >= min_size:
        font = pygame.font.SysFont("consolas", font_size)
        surface = font.render(text, True, color)
        if surface.get_width() <= max_width:
            return surface
        font_size -= 1

    font = pygame.font.SysFont("consolas", min_size)
    if max_width <= 0:
        return font.render("", True, color)

    clipped = text
    while clipped:
        candidate = clipped + "..."
        surface = font.render(candidate, True, color)
        if surface.get_width() <= max_width:
            return surface
        clipped = clipped[:-1]

    return font.render("", True, color)


def drawScoreBadge(screen, layout, blue_score, red_score, current_player):
    """Draw the top-center score badge."""
    badge_w = max(180, int(layout["width"] * 0.26))
    badge_h = max(44, int(layout["height"] * 0.08))
    badge_x = (layout["width"] - badge_w) // 2
    badge_y = max(8, layout["side_margin"] // 2)

    badge_rect = pygame.Rect(badge_x, badge_y, badge_w, badge_h)
    turn_color = BLUE_COLOR if current_player == PLAYER_BLUE else RED_COLOR

    pygame.draw.ellipse(screen, (240, 240, 238), badge_rect)
    pygame.draw.ellipse(screen, turn_color, badge_rect, 4)

    score_font = pygame.font.SysFont("consolas", max(20, int(badge_h * 0.48)), bold=True)
    blue_text = score_font.render(str(blue_score), True, BLUE_COLOR)
    dot_text = score_font.render(" - ", True, (40, 40, 40))
    red_text = score_font.render(str(red_score), True, RED_COLOR)

    score_w = blue_text.get_width() + dot_text.get_width() + red_text.get_width()
    score_h = max(blue_text.get_height(), dot_text.get_height(), red_text.get_height())
    score_surface = pygame.Surface((score_w, score_h), pygame.SRCALPHA)
    x = 0
    score_surface.blit(blue_text, (x, 0))
    x += blue_text.get_width()
    score_surface.blit(dot_text, (x, 0))
    x += dot_text.get_width()
    score_surface.blit(red_text, (x, 0))

    sx = badge_x + (badge_w - score_surface.get_width()) // 2
    sy = badge_y + (badge_h - score_surface.get_height()) // 2
    screen.blit(score_surface, (sx, sy))


def drawHud(screen, current_player, blue_score, red_score, winner, game_mode=None, difficulty=None, layout=None):
    """Draw the HUD areas around the board."""
    start_x = layout["board_x"]
    start_y = layout["board_y"]
    board_size = layout["board_size"]
    width = layout["width"]
    side_margin = layout["side_margin"]

    left_panel_width = max(120, start_x - side_margin * 2)
    right_panel_width = max(120, width - (start_x + board_size) - side_margin * 2)

    drawScoreBadge(screen, layout, blue_score, red_score, current_player)

    mode_name = "PVP" if game_mode == "pvp" else "PVBOT"
    difficulty_name = (difficulty or "easy").upper()
    if winner is None:
        status_lines = [f"Mode: {mode_name}", f"Bot: {difficulty_name}"]
    else:
        winner_name = "Blue" if winner == PLAYER_BLUE else "Red"
        status_lines = [f"Mode: {mode_name}", f"Bot: {difficulty_name}", f"Winner: {winner_name}"]

    left_x = side_margin
    left_y = start_y + 12
    for idx, line in enumerate(status_lines):
        line_surface = _render_fitted_line(
            line,
            HUD_TEXT_COLOR,
            preferred_size=max(16, int(layout["height"] * 0.032)),
            min_size=12,
            max_width=left_panel_width,
        )
        screen.blit(line_surface, (left_x, left_y + idx * 28))

    control_lines = ["M: Switch mode", "R: Restart", "1/2/3: EZ/MED/HARD"]
    right_x = start_x + board_size + side_margin
    right_y = start_y + 12
    for idx, line in enumerate(control_lines):
        line_surface = _render_fitted_line(
            line,
            HUD_TEXT_COLOR,
            preferred_size=max(16, int(layout["height"] * 0.032)),
            min_size=12,
            max_width=right_panel_width,
        )
        screen.blit(line_surface, (right_x, right_y + idx * 28))