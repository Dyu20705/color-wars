"""Main runtime loop: input, AI turn, and render."""

import pygame

from src.ai import get_ai_move
from src.controller import apply_move, get_scores
from src.engine.rules import PLAYER_BLUE, PLAYER_RED
from src.game.state import GameState
from src import view

MODE_PVP = "pvp"
MODE_PVBOT = "pvbot"
FPS = 60
EXPLOSION_ANIMATION_MS = 140


def run_game(game_mode=MODE_PVBOT):
    """Run one match in pvp or pvbot mode."""
    if game_mode not in (MODE_PVP, MODE_PVBOT):
        game_mode = MODE_PVBOT

    state = GameState()
    difficulty = "easy"

    is_fullscreen = False
    screen = view.drawScreen(fullscreen=is_fullscreen)
    clock = pygame.time.Clock()

    running = True

    def play_explosion_animation(steps):
        nonlocal running, screen, is_fullscreen
        if not steps:
            return

        frames_per_step = max(4, int(FPS * EXPLOSION_ANIMATION_MS / 1000))
        for step in steps:
            for frame in range(frames_per_step):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        return
                    if event.type == pygame.VIDEORESIZE and not is_fullscreen:
                        screen = view.drawScreen(fullscreen=False, size=event.size)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                        screen, is_fullscreen = view.toggle_fullscreen(is_fullscreen, screen)

                if not running:
                    return

                blue_score, red_score = get_scores(state)
                view.drawScene(
                    screen,
                    state.board,
                    state.dots,
                    state.current_player,
                    blue_score,
                    red_score,
                    state.winner,
                    game_mode,
                    difficulty,
                )
                progress = (frame + 1) / frames_per_step
                layout = view.compute_layout(screen, state.grid_size)
                view.drawExplosionOverlay(screen, layout, step, progress)
                pygame.display.flip()
                clock.tick(FPS)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
                screen = view.drawScreen(fullscreen=False, size=event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = GameState()
                elif event.key == pygame.K_m:
                    game_mode = MODE_PVP if game_mode == MODE_PVBOT else MODE_PVBOT
                    state = GameState()
                elif event.key == pygame.K_1:
                    difficulty = "easy"
                elif event.key == pygame.K_2:
                    difficulty = "medium"
                elif event.key == pygame.K_3:
                    difficulty = "hard"
                elif event.key == pygame.K_F11:
                    screen, is_fullscreen = view.toggle_fullscreen(is_fullscreen, screen)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_mode == MODE_PVP or state.current_player == PLAYER_BLUE:
                    row, col = view.get_cell_from_mouse(event.pos, state.grid_size, screen)
                    explosion_steps = []
                    moved = apply_move(
                        state,
                        row,
                        col,
                        explosion_callback=explosion_steps.append,
                    )
                    if moved:
                        play_explosion_animation(explosion_steps)

        if game_mode == MODE_PVBOT and state.winner is None and state.current_player == PLAYER_RED:
            move = get_ai_move(state.board, state.dots, difficulty)

            if move is None:
                blue_score, red_score = get_scores(state)
                if red_score == 0 and blue_score > 0:
                    state.winner = PLAYER_BLUE
                elif blue_score == 0 and red_score > 0:
                    state.winner = PLAYER_RED
                else:
                    state.current_player = PLAYER_BLUE
            else:
                explosion_steps = []
                moved = apply_move(
                    state,
                    move[0],
                    move[1],
                    player=PLAYER_RED,
                    explosion_callback=explosion_steps.append,
                )
                if moved:
                    play_explosion_animation(explosion_steps)

        blue_score, red_score = get_scores(state)
        view.drawScene(
            screen,
            state.board,
            state.dots,
            state.current_player,
            blue_score,
            red_score,
            state.winner,
            game_mode,
            difficulty,
        )

        pygame.display.flip()
        clock.tick(FPS)
