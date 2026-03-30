"""Render giao diện và ánh xạ input chuột cho Pygame UI."""

import pygame

from src.engine.rules import EMPTY, PLAYER_BLUE

HEIGHT = 600
WIDTH = 800

BOARD_SIZE = 500
NODE_SIZE = 100
BORDER_WIDTH = 1

BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_COLOR = (90, 188, 236)
RED_COLOR = (235, 112, 102)
HUD_TEXT_COLOR = (230, 230, 230)

def get_board_origin():
    """Trả về tọa độ góc trái trên của board (đặt giữa màn hình)."""
    start_x = (WIDTH - BOARD_SIZE) // 2
    start_y = (HEIGHT - BOARD_SIZE) // 2
    return start_x, start_y

def get_cell_from_mouse(mouse_pos, grid_size):
    """Đổi vị trí pixel chuột thành ô cờ; ngoài board thì trả về (None, None)."""
    start_x, start_y = get_board_origin()
    x, y = mouse_pos

    local_x = x - start_x
    local_y = y - start_y

    if local_x < 0 or local_y < 0:
        return None, None
    if local_x >= BOARD_SIZE or local_y >= BOARD_SIZE:
        return None, None

    col = local_x // NODE_SIZE
    row = local_y // NODE_SIZE

    if 0 <= row < grid_size and 0 <= col < grid_size:
        return row, col
    return None, None

def drawScreen():
    """Tạo cửa sổ game và đặt tiêu đề."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Color Wars")
    return screen


def drawScene(screen, board, dots, current_player, blue_score, red_score, winner, game_mode=None, difficulty=None):
    """Render một frame hoàn chỉnh"""
    screen.fill(BG_COLOR)
    drawBoard(screen, board, dots)
    drawHud(screen, current_player, blue_score, red_score, winner, game_mode, difficulty)


def drawBoard(screen, board, dots):
    """Vẽ grid board và tất cả ô đang có quân kèm số dot."""
    start_x, start_y = get_board_origin()
    grid_size = len(board)

    for row in range(grid_size):
        for col in range(grid_size):
            x = start_x + col * NODE_SIZE
            y = start_y + row * NODE_SIZE
            rect = (x, y, NODE_SIZE, NODE_SIZE)
            drawNode(screen, rect)

            if board[row][col] == EMPTY or dots[row][col] <= 0:
                continue

            color = BLUE_COLOR if board[row][col] == PLAYER_BLUE else RED_COLOR
            drawDot(screen, x, y, dots[row][col], color)


def drawNode(screen, rect):
    """Vẽ viền của một ô cờ."""
    pygame.draw.rect(screen, WHITE, rect, BORDER_WIDTH)


def drawDot(screen, x, y, count, color):
    """Vẽ mẫu dot cho 1..3; lớn hơn thì dùng bố cục fallback 4 góc."""
    cx = x + NODE_SIZE // 2
    cy = y + NODE_SIZE // 2
    radius = 10
    gap = 15

    if count == 1:
        positions = [(cx, cy)]
    elif count == 2:
        positions = [(cx - gap, cy), (cx + gap, cy)]
    elif count == 3:
        positions = [(cx - gap, cy), (cx + gap, cy), (cx, cy - gap)]
    else:
        positions = [
            (cx - gap, cy - gap),
            (cx + gap, cy - gap),
            (cx - gap, cy + gap),
            (cx + gap, cy + gap),
        ]

    for px, py in positions:
        pygame.draw.circle(screen, color, (px, py), radius)


def _render_fitted_line(text, color, preferred_size, min_size, max_width):
    """Render text vừa chiều rộng: giảm font hoặc cắt bằng dấu ba chấm."""
    font_size = preferred_size
    while font_size >= min_size:
        # Ưu tiên giữ nguyên nội dung bằng cách giảm dần cỡ chữ.
        font = pygame.font.SysFont("consolas", font_size)
        surface = font.render(text, True, color)
        if surface.get_width() <= max_width:
            return surface
        font_size -= 1

    font = pygame.font.SysFont("consolas", min_size)
    if max_width <= 0:
        return font.render("", True, color)

    clipped = text
    while clipped:
        # Nếu vẫn quá rộng ở cỡ nhỏ nhất thì cắt nội dung kèm "...".
        candidate = clipped + "..."
        surface = font.render(candidate, True, color)
        if surface.get_width() <= max_width:
            return surface
        clipped = clipped[:-1]

    return font.render("", True, color)


def drawHud(screen, current_player, blue_score, red_score, winner, game_mode=None, difficulty=None):
    """Vẽ HUD: điểm ở trên, trạng thái bên trái, phím tắt bên phải."""
    start_x, start_y = get_board_origin()
    board_center_x = start_x + BOARD_SIZE // 2
    side_margin = 16

    # Tính chiều rộng mỗi panel để text không tràn khi đổi kích thước cửa sổ.
    left_panel_width = max(120, start_x - side_margin * 2)
    right_panel_width = max(120, WIDTH - (start_x + BOARD_SIZE) - side_margin * 2)

    score_text = f"Blue: {blue_score}   Red: {red_score}"
    score_max_width = max(160, WIDTH - side_margin * 2)
    score_surface = _render_fitted_line(score_text, HUD_TEXT_COLOR, preferred_size=30, min_size=16, max_width=score_max_width)
    score_x = max(side_margin, board_center_x - score_surface.get_width() // 2)
    score_y = max(8, start_y - score_surface.get_height() - 10)

    mode_name = "PVP" if game_mode == "pvp" else "PVBOT"
    difficulty_name = (difficulty or "easy").upper()
    if winner is None:
        turn_name = "Blue" if current_player == PLAYER_BLUE else "Red"
        status_lines = [f"Mode: {mode_name}", f"Bot: {difficulty_name}", f"Turn: {turn_name}"]
    else:
        winner_name = "Blue" if winner == PLAYER_BLUE else "Red"
        status_lines = [f"Mode: {mode_name}", f"Bot: {difficulty_name}", f"Winner: {winner_name}"]

    #mode game
    
    left_x = side_margin
    left_y = start_y + 12
    for idx, line in enumerate(status_lines):
        line_surface = _render_fitted_line(line, HUD_TEXT_COLOR, preferred_size=22, min_size=14, max_width=left_panel_width)
        screen.blit(line_surface, (left_x, left_y + idx * 28))

    control_lines = ["M: Switch mode", "R: Restart", "1/2/3: EZ/MED/HARD"]
    right_x = start_x + BOARD_SIZE + side_margin
    right_y = start_y + 12
    for idx, line in enumerate(control_lines):
        line_surface = _render_fitted_line(line, HUD_TEXT_COLOR, preferred_size=22, min_size=14, max_width=right_panel_width)
        screen.blit(line_surface, (right_x, right_y + idx * 28))

    screen.blit(score_surface, (score_x, score_y))
