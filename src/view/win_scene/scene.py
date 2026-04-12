"""Win scene overlay renderer."""

import pygame

from src.engine.rules import PLAYER_BLUE


def draw_win_scene(screen, layout, winner):
    """Draw a winner banner above gameplay scene."""
    if winner is None:
        return

    width = layout["width"]
    panel_w = max(220, int(width * 0.34))
    panel_h = max(50, int(layout["height"] * 0.09))
    panel = pygame.Rect((width - panel_w) // 2, layout["top_hud_height"] + 8, panel_w, panel_h)

    pygame.draw.rect(screen, (255, 255, 255), panel, border_radius=18)
    border_color = (46, 125, 193) if winner == PLAYER_BLUE else (206, 79, 79)
    pygame.draw.rect(screen, border_color, panel, 3, border_radius=18)

    font = pygame.font.SysFont("consolas", max(18, int(panel_h * 0.38)), bold=True)
    winner_name = "BLUE" if winner == PLAYER_BLUE else "RED"
    text = font.render(f"{winner_name} WINS", True, border_color)
    screen.blit(text, text.get_rect(center=panel.center))
