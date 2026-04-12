"""Setting scene and icon renderer."""

import pygame


def draw_settings_icon(screen, rect, colors):
    """Draw a simple gear-like settings icon."""
    pygame.draw.circle(screen, colors["btn_slate"], rect.center, rect.width // 2)
    pygame.draw.circle(screen, (255, 255, 255), rect.center, rect.width // 2, 2)

    cx, cy = rect.center
    r_outer = max(7, rect.width // 4)
    r_inner = max(3, rect.width // 9)
    for angle in range(0, 360, 45):
        vx = int(cx + (r_outer + 3) * pygame.math.Vector2(1, 0).rotate(angle).x)
        vy = int(cy + (r_outer + 3) * pygame.math.Vector2(1, 0).rotate(angle).y)
        pygame.draw.circle(screen, (255, 255, 255), (vx, vy), 2)

    pygame.draw.circle(screen, (255, 255, 255), (cx, cy), r_outer, 2)
    pygame.draw.circle(screen, (255, 255, 255), (cx, cy), r_inner)


def draw_setting_scene(screen, panel, fonts, colors, back_rect, back_icon):
    """Draw settings scene content."""
    screen.blit(back_icon, back_rect.topleft)
    title = fonts["main"].render("Settings", True, colors["text_main"])
    subtitle = fonts["body"].render("Settings options will be expanded here.", True, colors["subtitle"])
    hint = fonts["body"].render("Current defaults: stable visuals, keyboard controls, local play.", True, colors["text_main"])

    screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 84)))
    screen.blit(subtitle, subtitle.get_rect(center=(panel.centerx, panel.y + 150)))
    screen.blit(hint, hint.get_rect(center=(panel.centerx, panel.y + 190)))
