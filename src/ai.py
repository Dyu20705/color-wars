import copy
import random
from collections import deque

EMPTY = 0
PLAYER_BLUE = 1
PLAYER_RED = 2


# kiểm tra ô trong board
def in_bounds(r, c, size):
    return 0 <= r < size and 0 <= c < size


# tính capacity của ô
def get_capacity(r, c, size):
    return 4


# BFS xử lý chain reaction
def resolve_explosions(board, dots, start_r, start_c):

    size = len(board)

    queue = deque([(start_r, start_c)])

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while queue:

        r, c = queue.popleft()

        owner = board[r][c]

        if owner == EMPTY:
            continue

        if dots[r][c] < get_capacity(r, c, size):
            continue

        dots[r][c] = 0
        board[r][c] = EMPTY

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if not in_bounds(nr, nc, size):
                continue

            board[nr][nc] = owner
            dots[nr][nc] += 1

            if dots[nr][nc] >= get_capacity(nr, nc, size):
                queue.append((nr, nc))


# tính điểm board
def evaluate(board):

    score = 0

    for row in board:
        for cell in row:

            if cell == PLAYER_RED:
                score += 1

            elif cell == PLAYER_BLUE:
                score -= 1

    return score


# tìm các move hợp lệ
def valid_moves(board, player):

    size = len(board)

    own_cells = []
    empty_cells = []

    for r in range(size):
        for c in range(size):

            if board[r][c] == player:
                own_cells.append((r,c))

            elif board[r][c] == EMPTY:
                empty_cells.append((r,c))

    # lượt đầu -> chỉ được chọn ô trống
    if len(own_cells) == 0:
        return empty_cells

    # các lượt sau -> chỉ được đánh ô của mình
    return own_cells


# AI chọn nước đi
def get_ai_move(board, dots):

    import random

    size = len(board)

    # ===== KIỂM TRA NƯỚC ĐẦU =====
    empty_cells = []

    for r in range(size):
        for c in range(size):
            if board[r][c] == EMPTY:
                empty_cells.append((r, c))

    # Nếu AI chưa có ô nào → random ô trống
    ai_has_cell = False
    for r in range(size):
        for c in range(size):
            if board[r][c] == PLAYER_RED:
                ai_has_cell = True

    if not ai_has_cell:
        return random.choice(empty_cells)

    # ===== AI LOGIC BÌNH THƯỜNG =====

    best_score = -9999
    best_move = None

    moves = valid_moves(board, PLAYER_RED)

    for r, c in moves:

        board_copy = copy.deepcopy(board)
        dots_copy = copy.deepcopy(dots)

        board_copy[r][c] = PLAYER_RED
        dots_copy[r][c] += 1

        resolve_explosions(board_copy, dots_copy, r, c)

        score = evaluate(board_copy)

        if score > best_score:
            best_score = score
            best_move = (r, c)

    return best_move