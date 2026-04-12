"""Tutorial scene and icon renderer."""

import pygame


def draw_tutorial_icon(screen, rect, colors, font):
    """Draw a circular question-mark button."""
    pygame.draw.circle(screen, colors["btn_amber"], rect.center, rect.width // 2)
    pygame.draw.circle(screen, (255, 255, 255), rect.center, rect.width // 2, 2)
    text = font.render("?", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=rect.center))


def draw_tutorial_scene(screen, panel, fonts, colors, back_rect, tutorial_lines, back_icon):
    """Draw tutorial content scene."""
    screen.blit(back_icon, back_rect.topleft)
    title = fonts["main"].render("Tutorial", True, colors["text_main"])
    screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 84)))

    line_y = panel.y + 130
    for line in tutorial_lines:
        text = fonts["body"].render(line, True, colors["text_main"])
        screen.blit(text, (panel.x + 28, line_y))
        line_y += max(22, int(panel.height * 0.06))
