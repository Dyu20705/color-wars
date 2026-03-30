"""Render giao diện và ánh xạ input chuột cho Pygame UI."""

import pygame

from src.engine.rules import EMPTY, PLAYER_BLUE

DEFAULT_HEIGHT = 600
DEFAULT_WIDTH = 800
BORDER_WIDTH = 1

BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_COLOR = (90, 188, 236)
RED_COLOR = (235, 112, 102)
HUD_TEXT_COLOR = (230, 230, 230)

def compute_layout(screen, grid_size):
    """Tính layout động theo kích thước màn hình hiện tại."""
    width, height = screen.get_size()
    side_margin = max(10, int(min(width, height) * 0.02))
    top_hud_height = max(48, int(height * 0.11))
    available_w = max(100, width - side_margin * 2)
    available_h = max(100, height - top_hud_height - side_margin)

    board_size = min(available_w, available_h)
    board_x = (width - board_size) // 2
    board_y = top_hud_height + (available_h - board_size) // 2
    cell_size = board_size / max(1, grid_size)

    return {
        "width": width,
        "height": height,
        "side_margin": side_margin,
        "top_hud_height": top_hud_height,
        "board_x": board_x,
        "board_y": board_y,
        "board_size": board_size,
        "cell_size": cell_size,
    }

def get_cell_from_mouse(mouse_pos, grid_size, screen):
    """Đổi vị trí pixel chuột thành ô cờ; ngoài board thì trả về (None, None)."""
    layout = compute_layout(screen, grid_size)
    start_x = layout["board_x"]
    start_y = layout["board_y"]
    board_size = layout["board_size"]
    cell_size = layout["cell_size"]
    x, y = mouse_pos

    local_x = x - start_x
    local_y = y - start_y

    if local_x < 0 or local_y < 0:
        return None, None
    if local_x >= board_size or local_y >= board_size:
        return None, None

    col = int(local_x // cell_size)
    row = int(local_y // cell_size)

    if 0 <= row < grid_size and 0 <= col < grid_size:
        return row, col
    return None, None

def drawScreen(fullscreen=False, size=(DEFAULT_WIDTH, DEFAULT_HEIGHT)):
    """Tạo cửa sổ game, hỗ trợ full screen và resize."""
    flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
    screen_size = (0, 0) if fullscreen else size
    screen = pygame.display.set_mode(screen_size, flags)
    pygame.display.set_caption("Color Wars")
    return screen

def toggle_fullscreen(is_fullscreen, screen):
    """Đổi chế độ fullscreen/windowed và trả về (screen mới, trạng thái mới)."""
    if is_fullscreen:
        return drawScreen(fullscreen=False), False
    return drawScreen(fullscreen=True), True


def drawScene(screen, board, dots, current_player, blue_score, red_score, winner, game_mode=None, difficulty=None):
    """Render một frame hoàn chỉnh"""
    layout = compute_layout(screen, len(board))
    screen.fill(BG_COLOR)
    drawBoard(screen, board, dots, layout)
    drawHud(screen, current_player, blue_score, red_score, winner, game_mode, difficulty, layout)


def drawBoard(screen, board, dots, layout):
    """Vẽ grid board và tất cả ô đang có quân kèm số dot."""
    start_x = layout["board_x"]
    start_y = layout["board_y"]
    cell_size = layout["cell_size"]
    grid_size = len(board)

    for row in range(grid_size):
        for col in range(grid_size):
            x = int(start_x + col * cell_size)
            y = int(start_y + row * cell_size)
            rect = (x, y, int(cell_size), int(cell_size))
            drawNode(screen, rect)

            if board[row][col] == EMPTY or dots[row][col] <= 0:
                continue

            color = BLUE_COLOR if board[row][col] == PLAYER_BLUE else RED_COLOR
            drawDot(screen, x, y, dots[row][col], color, cell_size)


def drawNode(screen, rect):
    """Vẽ viền của một ô cờ."""
    pygame.draw.rect(screen, WHITE, rect, BORDER_WIDTH)


def drawDot(screen, x, y, count, color, cell_size):
    """Vẽ mẫu dot cho 1..3; lớn hơn thì dùng bố cục fallback 4 góc."""
    cx = int(x + cell_size // 2)
    cy = int(y + cell_size // 2)
    radius = max(3, int(cell_size * 0.10))
    gap = max(6, int(cell_size * 0.17))

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


def _cell_center(layout, row, col):
    """Tính tâm pixel của một ô (row, col)."""
    cell_size = layout["cell_size"]
    cx = int(layout["board_x"] + col * cell_size + cell_size / 2)
    cy = int(layout["board_y"] + row * cell_size + cell_size / 2)
    return cx, cy


def drawExplosionOverlay(screen, layout, step, progress):
    """Vẽ hiệu ứng nổ theo tiến trình [0..1] cho một step."""
    if step is None:
        return

    center = step.get("center")
    targets = step.get("targets", [])
    owner = step.get("owner")
    if center is None:
        return

    base_color = BLUE_COLOR if owner == PLAYER_BLUE else RED_COLOR
    glow = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    cx, cy = _cell_center(layout, center[0], center[1])
    cell_size = layout["cell_size"]

    ring_radius = int(max(8, cell_size * (0.2 + 0.55 * progress)))
    ring_width = max(2, int(cell_size * 0.08))
    ring_alpha = max(0, int(190 * (1.0 - progress)))
    pygame.draw.circle(glow, (*base_color, ring_alpha), (cx, cy), ring_radius, ring_width)

    dot_radius = max(3, int(cell_size * 0.09))
    travel_alpha = max(0, int(220 * (1.0 - progress * 0.6)))
    for tr, tc in targets:
        tx, ty = _cell_center(layout, tr, tc)
        px = int(cx + (tx - cx) * progress)
        py = int(cy + (ty - cy) * progress)
        pygame.draw.circle(glow, (*base_color, travel_alpha), (px, py), dot_radius)

    screen.blit(glow, (0, 0))


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


def drawHud(screen, current_player, blue_score, red_score, winner, game_mode=None, difficulty=None, layout=None):
    """Vẽ HUD: điểm ở trên, trạng thái bên trái, phím tắt bên phải."""
    start_x = layout["board_x"]
    start_y = layout["board_y"]
    board_size = layout["board_size"]
    width = layout["width"]
    side_margin = layout["side_margin"]
    board_center_x = start_x + board_size // 2

    # Tính chiều rộng mỗi panel để text không tràn khi đổi kích thước cửa sổ.
    left_panel_width = max(120, start_x - side_margin * 2)
    right_panel_width = max(120, width - (start_x + board_size) - side_margin * 2)

    score_text = f"Blue: {blue_score}   Red: {red_score}"
    score_max_width = max(160, width - side_margin * 2)
    score_surface = _render_fitted_line(
        score_text,
        HUD_TEXT_COLOR,
        preferred_size=max(18, int(layout["height"] * 0.045)),
        min_size=14,
        max_width=score_max_width,
    )
    score_x = max(side_margin, board_center_x - score_surface.get_width() // 2)
    score_y = max(8, side_margin)

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
        line_surface = _render_fitted_line(
            line,
            HUD_TEXT_COLOR,
            preferred_size=max(16, int(layout["height"] * 0.032)),
            min_size=12,
            max_width=left_panel_width,
        )
        screen.blit(line_surface, (left_x, left_y + idx * 28))

    control_lines = ["M: Switch mode", "R: Restart", "1/2/3: EZ/MED/HARD"]
    right_x = start_x + board_size + side_margin
    right_y = start_y + 12
    for idx, line in enumerate(control_lines):
        line_surface = _render_fitted_line(
            line,
            HUD_TEXT_COLOR,
            preferred_size=max(16, int(layout["height"] * 0.032)),
            min_size=12,
            max_width=right_panel_width,
        )
        screen.blit(line_surface, (right_x, right_y + idx * 28))

    screen.blit(score_surface, (score_x, score_y))
