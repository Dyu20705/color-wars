"""Vòng lặp runtime chính: input, lượt AI, và render."""

import pygame

from src.ai import get_ai_move
from src.controller import apply_move, get_scores
from src.engine.rules import PLAYER_BLUE, PLAYER_RED
from src.game.state import GameState
from src import view

MODE_PVP = "pvp"
MODE_PVBOT = "pvbot"
FPS = 60


def run_game(game_mode=MODE_PVBOT):
    """Chạy một ván game ở mode pvp hoặc pvbot."""
    if game_mode not in (MODE_PVP, MODE_PVBOT):
        game_mode = MODE_PVBOT

    state = GameState()
    difficulty = "easy"

    screen = view.drawScreen()
    clock = pygame.time.Clock()

    running = True
    while running:
        # Xử lý input (thoát, phím tắt, click chuột).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # R: khởi tạo lại state để restart nhanh.
                if event.key == pygame.K_r:
                    state = GameState()
                # M: đổi mode rồi tạo ván mới để logic mode luôn nhất quán.
                elif event.key == pygame.K_m:
                    game_mode = MODE_PVP if game_mode == MODE_PVBOT else MODE_PVBOT
                    state = GameState()
                elif event.key == pygame.K_1:
                    difficulty = "easy"
                elif event.key == pygame.K_2:
                    difficulty = "medium"
                elif event.key == pygame.K_3:
                    difficulty = "hard"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Ở pvbot chỉ cho người chơi Blue click; pvp thì cả hai người.
                if game_mode == MODE_PVP or state.current_player == PLAYER_BLUE:
                    row, col = view.get_cell_from_mouse(event.pos, state.grid_size)
                    apply_move(state, row, col)

        # Lượt AI chỉ chạy trong pvbot, khi chưa có winner và tới lượt Red.
        if game_mode == MODE_PVBOT and state.winner is None and state.current_player == PLAYER_RED:
            move = get_ai_move(state.board, state.dots, difficulty)

            if move is None:
                # Không có nước đi hợp lệ: xử lý kết thúc ván hoặc nhường lượt.
                blue_score, red_score = get_scores(state)
                if red_score == 0 and blue_score > 0:
                    state.winner = PLAYER_BLUE
                elif blue_score == 0 and red_score > 0:
                    state.winner = PLAYER_RED
                else:
                    state.current_player = PLAYER_BLUE
            else:
                apply_move(state, move[0], move[1], player=PLAYER_RED)

        # Render frame hiện tại và khóa FPS ổn định.
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
