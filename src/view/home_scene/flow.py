"""Home menu scene for selecting mode and difficulty before a match."""

import pygame

from src.view.choose_diff_scene import draw_choose_diff_scene
from src.view.choose_gamemode_scene import draw_choose_gamemode_scene
from src.view.setting_scene import draw_setting_scene, draw_settings_icon
from src.view.tutorial_scene import draw_tutorial_icon, draw_tutorial_scene

from ..window import drawScreen
from .assets import get_home_asset_path, load_icon_or_placeholder, load_image
from .scene import draw_home_scene

MENU = "menu"
CHOOSE_MODE = "choose_mode"
DIFFICULTY = "difficulty"
TUTORIAL = "tutorial"
SETTINGS = "settings"
MODE_PVP = "pvp"
MODE_PVBOT = "pvbot"

HOME_BG_FALLBACK = (232, 242, 248)
TITLE_COLOR = (31, 69, 102)
SUBTITLE_COLOR = (63, 88, 105)
PANEL_COLOR = (248, 251, 253)
PANEL_BORDER = (166, 197, 218)
TEXT_MAIN = (31, 44, 54)
BTN_GREEN = (75, 165, 98)
BTN_AMBER = (233, 166, 73)
BTN_RED = (214, 91, 91)
BTN_BLUE = (72, 137, 196)
BTN_SLATE = (89, 114, 135)
DIFF_COLORS = {
    "easy": (80, 173, 100),
    "medium": (236, 172, 66),
    "hard": (213, 94, 89),
}


def difficulty_from_percent(percent):
    """Map slider percentage [0..1] to difficulty."""
    value = max(0.0, min(1.0, percent))
    if value < (1.0 / 3.0):
        return "easy"
    if value < (2.0 / 3.0):
        return "medium"
    return "hard"


def _difficulty_to_percent(difficulty):
    mapping = {"easy": 0.16, "medium": 0.5, "hard": 0.84}
    return mapping.get(difficulty, 0.16)


def _draw_button(screen, rect, label, color, font):
    pygame.draw.rect(screen, color, rect, border_radius=max(12, rect.height // 4))
    text = font.render(label, True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=rect.center))


def _draw_panel(screen, rect):
    pygame.draw.rect(screen, PANEL_COLOR, rect, border_radius=24)
    pygame.draw.rect(screen, PANEL_BORDER, rect, 2, border_radius=24)


def compute_menu_icon_rects(panel):
    """Return tutorial and settings icon rects for the home scene."""
    settings_icon_rect = pygame.Rect(panel.right - 58, panel.y + 16, 40, 40)
    tutorial_icon_rect = pygame.Rect(settings_icon_rect.x - 48, panel.y + 16, 40, 40)
    return tutorial_icon_rect, settings_icon_rect


def _draw_background(screen, cache):
    size = screen.get_size()
    cached_size = cache.get("size")
    if cached_size != size:
        image_path = get_home_asset_path("background.png")
        try:
            cache["image"] = load_image(image_path, size=size, alpha=False)
        except (pygame.error, FileNotFoundError, OSError):
            fallback = pygame.Surface(size)
            fallback.fill(HOME_BG_FALLBACK)
            cache["image"] = fallback
        cache["size"] = size

    screen.blit(cache["image"], (0, 0))
    overlay = pygame.Surface(size, pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 54))
    screen.blit(overlay, (0, 0))


def run_home_menu():
    """Run home flow and return selected configuration or None when user exits."""
    screen = drawScreen(fullscreen=False)
    clock = pygame.time.Clock()

    icon_size = (160, 160)
    icons = {
        "easy": load_icon_or_placeholder(get_home_asset_path("easy_icon.png"), icon_size, DIFF_COLORS["easy"]),
        "medium": load_icon_or_placeholder(get_home_asset_path("medium_icon.png"), icon_size, DIFF_COLORS["medium"]),
        "hard": load_icon_or_placeholder(get_home_asset_path("hard_icon.png"), icon_size, DIFF_COLORS["hard"]),
        "back": load_icon_or_placeholder(get_home_asset_path("back_icon.png"), (40, 40), BTN_SLATE),
    }

    bg_cache = {}

    state = MENU
    selected_mode = MODE_PVBOT
    difficulty = "easy"
    slider_percent = _difficulty_to_percent(difficulty)
    dragging = False

    while True:
        width, height = screen.get_size()
        title_font = pygame.font.SysFont("segoeui", max(34, int(height * 0.075)), bold=True)
        main_font = pygame.font.SysFont("segoeui", max(24, int(height * 0.05)), bold=True)
        btn_font = pygame.font.SysFont("segoeui", max(20, int(height * 0.033)), bold=True)
        body_font = pygame.font.SysFont("segoeui", max(16, int(height * 0.026)))

        panel = pygame.Rect(max(24, width // 10), max(30, height // 15), width - max(48, width // 5), height - max(60, height // 8))
        back_rect = pygame.Rect(panel.x + 18, panel.y + 16, 46, 46)

        tutorial_icon_rect, settings_icon_rect = compute_menu_icon_rects(panel)

        center_x = panel.centerx
        menu_btn_w = min(340, int(panel.width * 0.56))
        menu_btn_h = max(52, int(panel.height * 0.1))
        menu_start_y = panel.y + int(panel.height * 0.46)

        play_btn = pygame.Rect(center_x - menu_btn_w // 2, menu_start_y, menu_btn_w, menu_btn_h)
        quit_btn = pygame.Rect(center_x - menu_btn_w // 2, menu_start_y + menu_btn_h + 14, menu_btn_w, menu_btn_h)

        pvp_btn = pygame.Rect(center_x - menu_btn_w // 2, panel.y + int(panel.height * 0.45), menu_btn_w, menu_btn_h)
        pvbot_btn = pygame.Rect(center_x - menu_btn_w // 2, panel.y + int(panel.height * 0.45) + menu_btn_h + 16, menu_btn_w, menu_btn_h)

        slider_rect = pygame.Rect(center_x - min(180, panel.width // 3), panel.y + int(panel.height * 0.58), min(360, panel.width * 2 // 3), 22)
        knob_x = int(slider_rect.x + slider_rect.width * slider_percent)
        play_match_btn = pygame.Rect(center_x - menu_btn_w // 2, panel.bottom - menu_btn_h - 26, menu_btn_w, menu_btn_h)

        tutorial_lines = [
            "Objective: dominate the board by triggering chain explosions.",
            "Click a valid cell to place or reinforce your dots.",
            "You can only play empty cells on your first move.",
            "After that, you may only play your own cells.",
            "When a cell reaches 4 dots, it explodes and spreads.",
            "Controls:",
            "- Left Click: place or reinforce",
            "- M: switch PVP/PVBOT during match",
            "- R: restart current match",
            "- F11: toggle fullscreen",
        ]

        palette = {
            "title": TITLE_COLOR,
            "subtitle": SUBTITLE_COLOR,
            "text_main": TEXT_MAIN,
            "btn_green": BTN_GREEN,
            "btn_amber": BTN_AMBER,
            "btn_red": BTN_RED,
            "btn_blue": BTN_BLUE,
            "btn_slate": BTN_SLATE,
            "diff_colors": DIFF_COLORS,
        }

        shared_rects = {
            "draw_button": _draw_button,
            "back_rect": back_rect,
            "play_btn": play_btn,
            "quit_btn": quit_btn,
            "pvp_btn": pvp_btn,
            "pvbot_btn": pvbot_btn,
            "slider_rect": slider_rect,
            "knob_x": knob_x,
            "play_match_btn": play_match_btn,
            "settings_icon_rect": settings_icon_rect,
            "tutorial_icon_rect": tutorial_icon_rect,
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.VIDEORESIZE:
                screen = drawScreen(fullscreen=False, size=event.size)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if state == MENU:
                    return None
                if state in (CHOOSE_MODE, TUTORIAL):
                    state = MENU
                elif state == DIFFICULTY:
                    state = CHOOSE_MODE

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = event.pos
                if state == MENU:
                    if play_btn.collidepoint(mouse):
                        state = CHOOSE_MODE
                    elif tutorial_icon_rect.collidepoint(mouse):
                        state = TUTORIAL
                    elif settings_icon_rect.collidepoint(mouse):
                        state = SETTINGS
                    elif quit_btn.collidepoint(mouse):
                        return None

                elif state == CHOOSE_MODE:
                    if back_rect.collidepoint(mouse):
                        state = MENU
                    elif pvp_btn.collidepoint(mouse):
                        selected_mode = MODE_PVP
                        difficulty = "easy"
                        return {"game_mode": selected_mode, "difficulty": difficulty}
                    elif pvbot_btn.collidepoint(mouse):
                        selected_mode = MODE_PVBOT
                        state = DIFFICULTY

                elif state == DIFFICULTY:
                    if back_rect.collidepoint(mouse):
                        state = CHOOSE_MODE
                    elif play_match_btn.collidepoint(mouse):
                        return {"game_mode": selected_mode, "difficulty": difficulty}
                    elif slider_rect.collidepoint(mouse):
                        dragging = True
                        slider_percent = (mouse[0] - slider_rect.x) / max(1, slider_rect.width)
                        difficulty = difficulty_from_percent(slider_percent)
                    elif abs(mouse[0] - knob_x) <= 24 and abs(mouse[1] - slider_rect.centery) <= 24:
                        dragging = True

                elif state == TUTORIAL and back_rect.collidepoint(mouse):
                    state = MENU
                elif state == SETTINGS and back_rect.collidepoint(mouse):
                    state = MENU

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging and state == DIFFICULTY:
                slider_percent = (event.pos[0] - slider_rect.x) / max(1, slider_rect.width)
                difficulty = difficulty_from_percent(slider_percent)

        slider_percent = max(0.0, min(1.0, slider_percent))
        if not dragging:
            slider_percent = _difficulty_to_percent(difficulty)

        _draw_background(screen, bg_cache)
        _draw_panel(screen, panel)

        if state == MENU:
            draw_home_scene(
                screen,
                panel,
                {"title": title_font, "body": body_font, "button": btn_font},
                palette,
                shared_rects,
            )
            draw_settings_icon(screen, settings_icon_rect, palette)
            draw_tutorial_icon(screen, tutorial_icon_rect, palette, btn_font)

        elif state == CHOOSE_MODE:
            draw_choose_gamemode_scene(
                screen,
                panel,
                {"main": main_font, "button": btn_font},
                palette,
                shared_rects,
                icons["back"],
            )

        elif state == DIFFICULTY:
            shared_rects["knob_x"] = int(slider_rect.x + slider_rect.width * slider_percent)
            draw_choose_diff_scene(
                screen,
                panel,
                {"main": main_font, "body": body_font, "button": btn_font},
                palette,
                shared_rects,
                difficulty,
                icons,
            )

        elif state == TUTORIAL:
            draw_tutorial_scene(
                screen,
                panel,
                {"main": main_font, "body": body_font},
                palette,
                back_rect,
                tutorial_lines,
                icons["back"],
            )
        else:
            draw_setting_scene(
                screen,
                panel,
                {"main": main_font, "body": body_font},
                palette,
                back_rect,
                icons["back"],
            )

        pygame.display.flip()
        clock.tick(60)
