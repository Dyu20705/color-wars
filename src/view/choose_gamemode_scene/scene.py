"""Choose game mode scene renderer."""


def draw_choose_gamemode_scene(screen, panel, fonts, colors, rects, back_icon):
    """Draw mode selection scene."""
    screen.blit(back_icon, rects["back_rect"].topleft)
    title = fonts["main"].render("Select game mode", True, colors["text_main"])
    screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 110)))

    draw_button = rects["draw_button"]
    draw_button(screen, rects["pvp_btn"], "PLAYER VS PLAYER", colors["btn_blue"], fonts["button"])
    draw_button(screen, rects["pvbot_btn"], "PLAYER VS BOT", colors["btn_green"], fonts["button"])
