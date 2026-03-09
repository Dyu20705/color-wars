import pygame

HEIGHT = 600  # Chiều cao window
WIDTH = 800   # Chiều rộng window

BOARD_SIZE = 500  # Kích thước board (5 nodes x 100px)
NODE_SIZE = 100   # Kích thước mỗi ô
BORDER_WIDTH = 1  # Độ dày viền ô

BG_COLOR = (0, 0, 0)      # Màu nền: đen
WHITE = (255, 255, 255)   # Màu viền ô
BLUE_COLOR = (90, 188, 236)  # Màu dot xanh
RED_COLOR = (235, 112, 102)  # Màu dot đỏ

def drawScreen():
    # Khởi tạo cửa sổ game
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    SCREEN.fill(BG_COLOR)
    pygame.display.set_caption("Color Wars")
    return SCREEN

def drawBoard(SCREEN, BOARD, DOTS):
    # Tính toán vị trí bắt đầu
    start_x = (WIDTH - BOARD_SIZE) // 2
    start_y = (HEIGHT - BOARD_SIZE) // 2

    for i in range(5):
        for j in range(5):
            x = start_x + i * NODE_SIZE
            y = start_y + j * NODE_SIZE
            rect = (x, y, NODE_SIZE, NODE_SIZE)
            drawNode(SCREEN, rect)
            # Chỉ vẽ dot nếu ô còn thuộc về người chơi nào đó và có dot
            if BOARD[j][i] != 0 and DOTS[j][i] > 0:
                color = BLUE_COLOR if BOARD[j][i] == 1 else RED_COLOR
                drawDot(SCREEN, x, y, DOTS[j][i], color)

def drawNode(SCREEN, game):
    pygame.draw.rect(SCREEN, WHITE, game, BORDER_WIDTH)

def drawDot(SCREEN, x, y, count, color):
    cx = x + NODE_SIZE//2
    cy = y + NODE_SIZE//2

    if count == 1:
        pygame.draw.circle(SCREEN, color, (cx, cy), 10)
    elif count == 2:
        pygame.draw.circle(SCREEN, color, (cx-15, cy), 10)
        pygame.draw.circle(SCREEN, color, (cx+15, cy), 10)
    elif count == 3:
        pygame.draw.circle(SCREEN, color, (cx-15, cy), 10)
        pygame.draw.circle(SCREEN, color, (cx+15, cy), 10)
        pygame.draw.circle(SCREEN, color, (cx, cy-15), 10)