from collections import deque

import pygame
import view
import ai

GRID_SIZE = 5
EMPTY = 0
PLAYER_BLUE = 1
PLAYER_RED = 2
MIN_TURNS_FOR_WIN_CHECK = 2
FPS = 60

BOARD = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
DOTS = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

current_player = PLAYER_BLUE
turn_count = 0
winner = None
blue_has_occupied = False
red_has_occupied = False


def in_bounds(row, col):
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE


def get_cell_capacity(row, col):
    return 4


def get_scores():
    blue_cells = 0
    red_cells = 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if BOARD[row][col] == PLAYER_BLUE:
                blue_cells += 1
            elif BOARD[row][col] == PLAYER_RED:
                red_cells += 1
    return blue_cells, red_cells


def update_winner():
    global winner, blue_has_occupied, red_has_occupied
    blue_cells, red_cells = get_scores()

    # Phải có ít nhất 1 ô mới được chơi tiếp
    if blue_cells > 0:
        blue_has_occupied = True
    if red_cells > 0:
        red_has_occupied = True

    # Tránh kết thúc ván quá sớm trước khi hai bên nhập cuộc.
    if turn_count < MIN_TURNS_FOR_WIN_CHECK:
        return

    # Một bên bị ăn sạch (đã từng có quân nhưng hiện không còn ô nào) => thua.
    if blue_has_occupied and blue_cells == 0 and red_cells > 0:
        winner = PLAYER_RED
    elif red_has_occupied and red_cells == 0 and blue_cells > 0:
        winner = PLAYER_BLUE


def resolve_explosions(start_row, start_col):
    queue = deque([(start_row, start_col)])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        row, col = queue.popleft()
        owner = BOARD[row][col]
        if owner == EMPTY:
            continue

        if DOTS[row][col] < get_cell_capacity(row, col):
            continue

        DOTS[row][col] = 0
        BOARD[row][col] = EMPTY

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if not in_bounds(nr, nc):
                continue

            # Đồng hóa mục tiêu
            BOARD[nr][nc] = owner
            DOTS[nr][nc] += 1

            if DOTS[nr][nc] >= get_cell_capacity(nr, nc):
                queue.append((nr, nc))


def try_place_dot(mouse_pos):
    global current_player, turn_count

    if winner is not None:
        return

    row, col = view.get_cell_from_mouse(mouse_pos, GRID_SIZE)

    if row is None or col is None:
        return

    # kiểm tra player đã có ô nào chưa
    has_cell = False
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if BOARD[r][c] == current_player:
                has_cell = True
                break

    # nếu chưa có ô -> lượt đầu -> chỉ được chọn ô trống
    if not has_cell:
        if BOARD[row][col] != EMPTY:
            return

    # nếu đã có ô -> chỉ được đánh vào ô của mình
    else:
        if BOARD[row][col] != current_player:
            return

    BOARD[row][col] = current_player
    DOTS[row][col] += 1

    resolve_explosions(row, col)

    turn_count += 1
    update_winner()

    if winner is None:
        current_player = PLAYER_RED if current_player == PLAYER_BLUE else PLAYER_BLUE

# def runGame():
#     screen = view.drawScreen()
#     clock = pygame.time.Clock()

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 try_place_dot(event.pos)

#         blue_score, red_score = get_scores()
#         view.drawScene(screen, BOARD, DOTS, current_player, blue_score, red_score, winner)
#         pygame.display.flip()
#         clock.tick(FPS)
def runGame():
    global current_player, turn_count

    screen = view.drawScreen()
    clock = pygame.time.Clock()

    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # người chơi (Blue)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if current_player == PLAYER_BLUE:
                    try_place_dot(event.pos)

        # ===== AI TURN =====
        if winner is None and current_player == PLAYER_RED:

            move = ai.get_ai_move(BOARD, DOTS)

            if move is not None:

                r, c = move

                BOARD[r][c] = PLAYER_RED
                DOTS[r][c] += 1

                resolve_explosions(r, c)

                turn_count += 1
                update_winner()

                if winner is None:
                    current_player = PLAYER_BLUE

        blue_score, red_score = get_scores()

        view.drawScene(screen, BOARD, DOTS, current_player, blue_score, red_score, winner)

        pygame.display.flip()
        clock.tick(FPS)