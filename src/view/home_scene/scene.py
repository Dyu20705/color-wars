"""Home scene renderer."""

from src.view.commons import blit_fitted_text


def _blit_shadow_text(screen, font, text, color, center, shadow_color=(10, 14, 22), offset=(2, 2)):
    """Draw text with subtle shadow to keep readability on busy backgrounds."""
    shadow_pos = (center[0] + offset[0], center[1] + offset[1])
    max_width = int(screen.get_width() * 0.8)
    max_height = max(24, int(font.get_height() * 1.1))
    blit_fitted_text(screen, font, text, shadow_color, shadow_pos, max_width, max_height)
    blit_fitted_text(screen, font, text, color, center, max_width, max_height)


def draw_home_scene(screen, panel, fonts, colors, rects):
    """Draw the main home scene."""
    center_x = panel.centerx
    _blit_shadow_text(screen, fonts["title"], "COLOR WARS", colors["title"], (center_x, panel.y + 88))
    _blit_shadow_text(
        screen,
        fonts["body"],
        "Dễ làm quen, khó tinh thông",
        colors["subtitle"],
        (center_x, panel.y + 138),
        shadow_color=(10, 14, 22),
        offset=(1, 1),
    )

    # draw_button = rects["draw_button"]
    # draw_button(screen, rects["play_btn"], "CHƠI", colors["btn_green"], fonts["button"])
    # draw_button(screen, rects["quit_btn"], "THOÁT", colors["btn_red"], fonts["button"])
