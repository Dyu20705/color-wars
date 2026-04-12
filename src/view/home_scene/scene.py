"""Home scene renderer."""


def draw_home_scene(screen, panel, fonts, colors, rects):
    """Draw the main home scene."""
    center_x = panel.centerx
    title = fonts["title"].render("COLOR WARS", True, colors["title"])
    subtitle = fonts["body"].render("Plan your match before entering the board", True, colors["subtitle"])
    screen.blit(title, title.get_rect(center=(center_x, panel.y + 88)))
    screen.blit(subtitle, subtitle.get_rect(center=(center_x, panel.y + 138)))

    draw_button = rects["draw_button"]
    draw_button(screen, rects["play_btn"], "PLAY", colors["btn_green"], fonts["button"])
    draw_button(screen, rects["quit_btn"], "QUIT", colors["btn_red"], fonts["button"])
