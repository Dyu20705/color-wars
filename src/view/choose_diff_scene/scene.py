"""Choose difficulty scene renderer."""

import pygame


def draw_choose_diff_scene(screen, panel, fonts, colors, rects, difficulty, icons):
    """Draw difficulty picker scene."""
    screen.blit(icons["back"], rects["back_rect"].topleft)

    current_color = colors["diff_colors"][difficulty]
    icon = icons[difficulty]
    screen.blit(icon, icon.get_rect(center=(panel.centerx, panel.y + 170)))

    diff_label = fonts["main"].render(difficulty.upper(), True, current_color)
    screen.blit(diff_label, diff_label.get_rect(center=(panel.centerx, panel.y + 270)))

    slider_rect = rects["slider_rect"]
    knob_x = rects["knob_x"]
    pygame.draw.rect(screen, (218, 226, 232), slider_rect, border_radius=14)
    fill_rect = pygame.Rect(slider_rect.x, slider_rect.y, max(1, knob_x - slider_rect.x), slider_rect.height)
    pygame.draw.rect(screen, current_color, fill_rect, border_radius=14)
    pygame.draw.circle(screen, (255, 255, 255), (knob_x, slider_rect.centery), 15)
    pygame.draw.circle(screen, current_color, (knob_x, slider_rect.centery), 11)

    tip = fonts["body"].render("Slide to choose bot difficulty", True, colors["subtitle"])
    screen.blit(tip, tip.get_rect(center=(panel.centerx, slider_rect.bottom + 28)))

    rects["draw_button"](screen, rects["play_match_btn"], "START MATCH", current_color, fonts["button"])
