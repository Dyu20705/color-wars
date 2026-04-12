import pygame

# Khởi tạo
pygame.init()
WIDTH, HEIGHT = 450, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Wars - Background Update")

# --- PHẦN 1: TỐI ƯU LOAD ẢNH & BACKGROUND ---
def load_and_scale(name, size=(180, 180)):
    try:
        img = pygame.image.load(name).convert_alpha()
        return pygame.transform.smoothscale(img, size)
    except:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(surf, (200, 200, 200), (size[0]//2, size[1]//2), size[0]//2)
        return surf

# Nạp Background
# Bạn hãy thay 'bg_main.png' bằng tên file ảnh nền của bạn
try:
    bg_image = pygame.image.load('bg_main.png').convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
    # Nếu chưa có file ảnh, dùng màu xanh nhạt làm nền
    bg_image = pygame.Surface((WIDTH, HEIGHT))
    bg_image.fill((240, 245, 250))

# Nạp Icons
img_easy = load_and_scale('src/home/easy_icon.png')
img_medium = load_and_scale('src/home/medium_icon.png')
img_hard = load_and_scale('src/home/hard_icon.png')
img_back = load_and_scale('src/home/back_icon.png', (45, 45))

# --- PHẦN 2: FONT & STATE ---
try:
    font_path = "C:/Windows/Fonts/tahoma.ttf"
    font_title = pygame.font.Font(font_path, 55)
    font_btn = pygame.font.Font(font_path, 20)
    font_main = pygame.font.Font(font_path, 45)
except:
    font_title = pygame.font.SysFont("Arial", 55, bold=True)
    font_btn = pygame.font.SysFont("Arial", 20, bold=True)
    font_main = pygame.font.SysFont("Arial", 45, bold=True)

game_state = "MENU" 
COLORS = {
    "EASY": (134, 190, 72), "MEDIUM": (241, 180, 52),
    "HARD": (232, 110, 91), "BLUE": (70, 130, 180),
    "DARK_GRAY": (60, 60, 60)
}

slider_rect = pygame.Rect(WIDTH//2 - 125, 480, 250, 35)
knob_x = slider_rect.x + 20
current_diff = "EASY"
dragging = False

running = True
while running:
    mouse_p = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "MENU":
                if WIDTH//2 - 120 < mouse_p[0] < WIDTH//2 + 120:
                    if 350 < mouse_p[1] < 425: game_state = "CHOOSE_MODE"
                    elif 550 < mouse_p[1] < 625: running = False
            elif game_state == "CHOOSE_MODE":
                if mouse_p[0] < 70 and mouse_p[1] < 70: game_state = "MENU"
                if WIDTH//2 - 120 < mouse_p[0] < WIDTH//2 + 120:
                    if 450 < mouse_p[1] < 525: game_state = "DIFFICULTY"
            elif game_state == "DIFFICULTY":
                if mouse_p[0] < 70 and mouse_p[1] < 70: game_state = "CHOOSE_MODE"
                if abs(mouse_p[0] - knob_x) < 30 and abs(mouse_p[1] - slider_rect.centery) < 30:
                    dragging = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    if game_state == "DIFFICULTY" and dragging:
        knob_x = max(slider_rect.left, min(mouse_p[0], slider_rect.right))
        percent = (knob_x - slider_rect.x) / slider_rect.width
        if percent < 0.33: current_diff = "EASY"
        elif percent < 0.66: current_diff = "MEDIUM"
        else: current_diff = "HARD"

    # --- VẼ ---
    # BƯỚC QUAN TRỌNG: Luôn vẽ background đầu tiên
    screen.blit(bg_image, (0, 0))

    if game_state == "MENU":
        # Vẽ một lớp phủ mờ (Overlay) nếu background quá sáng làm mờ chữ
        # overlay = pygame.Surface((WIDTH, HEIGHT))
        # overlay.set_alpha(100) # Độ mờ
        # overlay.fill((255, 255, 255))
        # screen.blit(overlay, (0, 0))

        title = font_title.render("COLOR WARS", True, COLORS["BLUE"])
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        for txt, y, col in [("CHƠI", 350, COLORS["EASY"]), ("HƯỚNG DẪN", 450, COLORS["MEDIUM"]), ("THOÁT", 550, COLORS["HARD"])]:
            rect = pygame.Rect(WIDTH//2 - 120, y, 240, 75)
            pygame.draw.rect(screen, col, rect, border_radius=15)
            s = font_btn.render(txt, True, (255, 255, 255))
            screen.blit(s, (rect.centerx - s.get_width()//2, rect.centery - s.get_height()//2))

    elif game_state == "CHOOSE_MODE":
        screen.blit(img_back, (20, 20))
        title = font_main.render("CHẾ ĐỘ CHƠI", True, COLORS["DARK_GRAY"])
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        modes = [("CHƠI VỚI NGƯỜI", 350, COLORS["BLUE"]), ("CHƠI VỚI MÁY", 450, COLORS["EASY"])]
        for txt, y, col in modes:
            rect = pygame.Rect(WIDTH//2 - 130, y, 260, 75)
            pygame.draw.rect(screen, col, rect, border_radius=15)
            s = font_btn.render(txt, True, (255, 255, 255))
            screen.blit(s, (rect.centerx - s.get_width()//2, rect.centery - s.get_height()//2))

    elif game_state == "DIFFICULTY":
        theme_col = COLORS[current_diff]
        screen.blit(img_back, (20, 20))
        curr_img = {"EASY": img_easy, "MEDIUM": img_medium, "HARD": img_hard}[current_diff]
        screen.blit(curr_img, curr_img.get_rect(center=(WIDTH//2, 230)))
        
        txt = font_main.render(current_diff, True, theme_col)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 360))
        
        pygame.draw.rect(screen, (210, 210, 210), slider_rect, border_radius=20)
        pygame.draw.rect(screen, theme_col, (slider_rect.x, slider_rect.y, knob_x - slider_rect.x, slider_rect.height), border_radius=20)
        pygame.draw.circle(screen, (255, 255, 255), (int(knob_x), slider_rect.centery), 22)
        pygame.draw.circle(screen, theme_col, (int(knob_x), slider_rect.centery), 16)
        
        lbl = font_btn.render("CHỌN ĐỘ KHÓ", True, (100, 100, 100))
        screen.blit(lbl, (WIDTH//2 - lbl.get_width()//2, slider_rect.bottom + 15))

        btn = pygame.Rect(WIDTH//2 - 100, 650, 200, 75)
        pygame.draw.rect(screen, theme_col, btn, border_radius=38)
        p_txt = font_main.render("PLAY", True, (255, 255, 255))
        screen.blit(p_txt, (btn.centerx - p_txt.get_width()//2, btn.centery - p_txt.get_height()//2))

    pygame.display.flip()

pygame.quit()